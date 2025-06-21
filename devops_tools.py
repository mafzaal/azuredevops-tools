"""
devops_tools.py

A toolset for interacting with Azure DevOps TFVC, designed for use with LangChain or other modular pipelines.
Extracted from GenerateReleaseNotes.py for reuse and separation of concerns.
"""
import os
import logging
from dotenv import load_dotenv
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v7_0.tfvc.models import TfvcChange,TfvcVersionDescriptor,TfvcChangesetSearchCriteria
from azure.devops.v7_0.build.models import Build

from datetime import datetime
from typing import List, Dict, Any, Optional


class DevOpsToolset:
    """A toolset for Azure DevOps TFVC operations."""
    def __init__(self):
        load_dotenv()
        self.pat = os.getenv("DEVOPS_PAT")
        self.organization = os.getenv("DEVOPS_ORGANIZATION")
        self.project = os.getenv("DEVOPS_PROJECT")
        if not all([self.pat, self.organization, self.project]):
            raise ValueError("Missing required Azure DevOps environment variables")
        organization_url = f"https://dev.azure.com/{self.organization}"
        credentials = BasicAuthentication('', self.pat or '')
        self.connection = Connection(base_url=organization_url, creds=credentials)
        self.tfvc_client = self.connection.clients.get_tfvc_client()
        self.build_client = self.connection.clients.get_build_client()

    def get_changeset_list(self, author: Optional[str] = None, from_changeset_id: Optional[int] = None, to_changeset_id: Optional[int] = None):
        """Retrieve changesets using azure-devops SDK."""
        logging.info(f"Retrieving changesets since ID {from_changeset_id} for author {author}...")
        search_criteria = TfvcChangesetSearchCriteria()
        if author:
            search_criteria.author = author
        if from_changeset_id:
            search_criteria.from_id = from_changeset_id
        
        if to_changeset_id:
            search_criteria.to_id = to_changeset_id

        changesets = self.tfvc_client.get_changesets(
            project=self.project,
            search_criteria=search_criteria,
        )
        result = []
        
        for cs in changesets:
            result.append({
                'changesetId': cs.changeset_id,
                'comment': cs.comment,
                'author': {'displayName': cs.author.display_name if cs.author else 'Unknown'},
                'createdDate': cs.created_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if cs.created_date else 'Unknown date'
            })
        logging.info(f"Found {len(result)} changesets after ID {from_changeset_id}.")
        return result
    
    def get_changeset(self, changeset_id):
        """Retrieve a specific changeset by ID."""
        try:
            changeset = self.tfvc_client.get_changeset(changeset_id, project=self.project)
            return {
                'changesetId': changeset.changeset_id,
                'comment': changeset.comment,
                'author': {'displayName': changeset.author.display_name if changeset.author else 'Unknown'},
                'createdDate': changeset.created_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if changeset.created_date else 'Unknown date'
            }
        except Exception as e:
            logging.error(f"Error retrieving changeset {changeset_id}: {e}")
            return None
    
    def get_changeset_changes(self, changeset_id):
        """Get the files changed in a specific changeset."""
        try:
            changes: List[TfvcChange] = self.tfvc_client.get_changeset_changes(id=changeset_id)
            
            
            result = []
            for ch in changes:
                # Access data from additional_properties since direct attributes are None
                item_data = ch.additional_properties.get('item', {})
                change_type = ch.additional_properties.get('changeType', 'unknown')
                
                #logging.info(f"Item: {item_data}")
                result.append( {
                        'path': item_data.get('path', 'Unknown path'),
                        'changeType': change_type,
                        'version': item_data.get('version'),
                        'size': item_data.get('size'),
                        'url': item_data.get('url')
                    }
                )
            return result
        except Exception as e:
            logging.error(f"Error retrieving changes for changeset {changeset_id}: {e}")
            return []

    def get_file_content(self, file_path, changeset_id,version_option='None'):
        """Get content of a file at a specific changeset."""
        try:
            version_descriptor= TfvcVersionDescriptor(str(changeset_id),version_option,'changeset')

            chunks = self.tfvc_client.get_item_content(
                path=file_path,
                version_descriptor=version_descriptor,
                project=self.project,
                download=True
            )

            
            content = ""
            for chunk in  chunks:
                content += chunk.decode('utf-8', errors='ignore')

            return content if content else ''

        except Exception as e:
            logging.error(f"Error retrieving content for {file_path} at changeset {changeset_id}: {e}")
            return ""

    def get_file_diff(self, file_path, changeset_id):
        """Get diff of file changes in a specific changeset."""
        try:
            current_content = self.get_file_content(file_path, changeset_id)
            previous_content = self.get_file_content(file_path, changeset_id,version_option='Previous')
            if not previous_content:
                return f"New file: {file_path}\n\n{current_content}"
            
            # generate git style diff
            if not current_content:
                return f"Deleted file: {file_path}\n\nPrevious version:\n{previous_content}"
            if current_content == previous_content:
                return f"No changes in file: {file_path}"
            # Simple diff representation
            current_lines = current_content.splitlines()
            previous_lines = previous_content.splitlines()

            import difflib

            diffs = difflib.unified_diff(previous_lines, current_lines)
            diff_output = '\n'.join(diffs)

            if not diff_output:
                return f"No changes in file: {file_path}"
            
            return f"Diff: {file_path}\n\n{diff_output}"
          
           
        except Exception as e:
            logging.error(f"Error calculating diff for {file_path} at changeset {changeset_id}: {e}")
            return f"Modified file: {file_path}\n\nError retrieving diff: {str(e)}"


    def format_changeset_summary(self, changeset):
        """Format a single changeset summary for reporting."""
        changeset_id = changeset.get('changesetId')
        comment = changeset.get('comment', 'No comment')
        author = changeset.get('author', {}).get('displayName', 'Unknown')
        created_date = changeset.get('createdDate', 'Unknown date')
        if isinstance(created_date, str):
            try:
                created_date = datetime.strptime(created_date, "%Y-%m-%dT%H:%M:%S.%fZ")
                created_date = created_date.strftime("%Y-%m-%d %H:%M:%S")
            except:
                pass
        summary = f"""
        Changeset {changeset_id} by {author} on {created_date}
        Comment: {comment}
        {'-' * 40}
        """
        return summary

    def get_build(self, build_id: int) -> Dict[str, Any]:
        """
        Retrieve details about a specific build.
        
        Args:
            build_id: The ID of the build to retrieve
            
        Returns:
            Dictionary containing build information including status and result
        """
        try:
            logging.info(f"Retrieving build {build_id}...")
            build: Build = self.build_client.get_build(project=self.project, build_id=build_id)
            
            result = {
                'id': build.id,
                'buildNumber': build.build_number,
                'status': build.status,
                'result': build.result,
                'queueTime': build.queue_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if build.queue_time else None,
                'startTime': build.start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if build.start_time else None,
                'finishTime': build.finish_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if build.finish_time else None,
                'reason': build.reason,
                'requestedFor': build.requested_for.display_name if build.requested_for else 'Unknown',
                'definition': {
                    'id': build.definition.id,
                    'name': build.definition.name
                } if build.definition else None,
                'url': build.url
            }
            return result
        except Exception as e:
            logging.error(f"Error retrieving build {build_id}: {e}")
            return {'error': str(e)}
            
    def get_builds(self, definition_id: Optional[int] = None, top: int = 50, status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve multiple builds from the project.
        
        Args:
            definition_id: Optional definition ID to filter builds by specific pipeline
            top: Maximum number of builds to retrieve (default 50)
            status_filter: Optional status filter ('completed', 'inProgress', 'notStarted')
            
        Returns:
            List of dictionaries containing build information
        """
        try:
            logging.info(f"Retrieving up to {top} builds...")
            
            builds = self.build_client.get_builds(
                project=self.project,
                definitions=[definition_id] if definition_id else None,
                top=top,
                status_filter=status_filter
            )
            
            result = []
            for build in builds:
                build_info = {
                    'id': build.id,
                    'buildNumber': build.build_number,
                    'status': build.status,
                    'result': build.result,
                    'queueTime': build.queue_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if build.queue_time else None,
                    'startTime': build.start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if build.start_time else None,
                    'finishTime': build.finish_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if build.finish_time else None,
                    'reason': build.reason,
                    'requestedFor': build.requested_for.display_name if build.requested_for else 'Unknown',
                    'definition': {
                        'id': build.definition.id,
                        'name': build.definition.name
                    } if build.definition else None,
                    'url': build.url
                }
                result.append(build_info)
                
            return result
        except Exception as e:
            logging.error(f"Error retrieving builds: {e}")
            return [{'error': str(e)}]

    def get_build_logs(self, build_id: int) -> List[Dict[str, Any]]:
        """
        Retrieve logs for a specific build.
        
        Args:
            build_id: The ID of the build to retrieve logs for
            
        Returns:
            List of dictionaries containing log information and content
        """
        try:
            logging.info(f"Retrieving logs for build {build_id}...")
            logs = self.build_client.get_build_logs(project=self.project, build_id=build_id)
            
            result = []
            for log in logs:
                log_content = self.build_client.get_build_log_lines(
                    project=self.project, 
                    build_id=build_id, 
                    log_id=log.id
                )
                
                result.append({
                    'id': log.id,
                    'type': log.type,
                    'url': log.url,
                    'createdOn': log.created_on.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if log.created_on else None,
                    'lastChangedOn': log.last_changed_on.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if log.last_changed_on else None,
                    'content': log_content
                })
                
            return result
        except Exception as e:
            logging.error(f"Error retrieving logs for build {build_id}: {e}")
            return [{'error': str(e)}]

    def f1e_get_build_tool(self, build_id: int) -> str:
        """
        LLM-friendly tool to retrieve build status and details.
        
        This tool retrieves a specific build and formats the details in a human-readable string format
        that's suitable for LLM consumption.
        
        Parameters:
            build_id (int): The ID of the build to retrieve
            
        Returns:
            str: A formatted string with details about the build including status and result
        """
        build_info = self.get_build(build_id)
        
        if 'error' in build_info:
            return f"Error retrieving build {build_id}: {build_info['error']}"
        
        # Format the build information as a string suitable for LLM consumption
        result = f"Build {build_info['id']} ({build_info['buildNumber']}):\n"
        result += f"Status: {build_info['status']}\n"
        result += f"Result: {build_info['result']}\n"
        result += f"Requested by: {build_info['requestedFor']}\n"
        result += f"Reason: {build_info['reason']}\n"
        
        if build_info['definition']:
            result += f"Definition: {build_info['definition']['name']} (ID: {build_info['definition']['id']})\n"
        
        if build_info['queueTime']:
            result += f"Queue time: {build_info['queueTime']}\n"
        
        if build_info['startTime']:
            result += f"Start time: {build_info['startTime']}\n"
        
        if build_info['finishTime']:
            result += f"Finish time: {build_info['finishTime']}\n"
            
            # Calculate duration if start and finish times are available
            try:
                start = datetime.strptime(build_info['startTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
                finish = datetime.strptime(build_info['finishTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
                duration = finish - start
                result += f"Duration: {duration}\n"
            except (ValueError, TypeError):
                pass
        
        return result    
    
    def f1e_get_builds_tool(self, definition_id: Optional[int] = None, top: int = 50, status_filter: Optional[str] = None) -> str:
        """
        LLM-friendly tool to retrieve multiple builds.
        
        This tool retrieves multiple builds and formats them in a human-readable string format
        suitable for LLM consumption.
        
        Parameters:
            definition_id (int, optional): Filter builds by specific pipeline/definition ID
            top (int): Maximum number of builds to retrieve (default 50)
            status_filter (str, optional): Filter by status ('completed', 'inProgress', 'notStarted')
            
        Returns:
            str: A formatted string with details about multiple builds
        """
        builds = self.get_builds(definition_id, top, status_filter)
        
        if builds and 'error' in builds[0]:
            return f"Error retrieving builds: {builds[0]['error']}"
        
        if not builds:
            return "No builds found matching the criteria."
        
        result = f"Found {len(builds)} build(s):\n\n"
        
        for build in builds:
            result += f"Build {build['id']} ({build['buildNumber']}):\n"
            result += f"  Status: {build['status']}\n"
            result += f"  Result: {build['result']}\n"
            result += f"  Requested by: {build['requestedFor']}\n"
            
            if build['definition']:
                result += f"  Pipeline: {build['definition']['name']} (ID: {build['definition']['id']})\n"
            
            if build['startTime']:
                result += f"  Start time: {build['startTime']}\n"
            
            if build['finishTime']:
                result += f"  Finish time: {build['finishTime']}\n"
                
                # Calculate duration if start and finish times are available
                try:
                    start = datetime.strptime(build['startTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
                    finish = datetime.strptime(build['finishTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
                    duration = finish - start
                    result += f"  Duration: {duration}\n"
                except (ValueError, TypeError):
                    pass
            
            result += "-" * 50 + "\n"
        
        return result

    def f1e_get_build_logs_tool(self, build_id: int) -> Dict[str, Any]:
        """
        LLM-friendly tool to retrieve build logs summary with last 50 lines of content.

        This tool retrieves logs for a specific build and returns them as a structured
        dictionary object with metadata and last 50 lines of content for each log.

        Parameters:
            build_id (int): The ID of the build to retrieve logs for

        Returns:
            Dict[str, Any]: A dictionary containing build logs with metadata and preview content
        """
        logs = self.get_build_logs(build_id)

        if logs and 'error' in logs[0]:
            return {
                'buildId': build_id,
                'error': logs[0]['error'],
                'logs': []
            }

        if not logs:
            return {
                'buildId': build_id,
                'totalLogs': 0,
                'logs': []
            }

        # Structure the logs as objects with preview content (last 50 lines)
        structured_logs = []
        for log in logs:
            content_lines = log.get('content', [])
            preview_lines = content_lines[-50:]  # Last 50 lines only

            log_obj = {
                'id': log['id'],
                'type': log['type'],
                'url': log.get('url'),
                'createdOn': log.get('createdOn'),
                'lastChangedOn': log.get('lastChangedOn'),
                'contentLines': preview_lines,
                'contentLineCount': len(content_lines),  # Total count, not preview count
                'previewContent': '\n'.join(preview_lines),
                'hasMoreContent': len(content_lines) > 50
            }
            structured_logs.append(log_obj)

        return {
            'buildId': build_id,
            'totalLogs': len(structured_logs),
            'logs': structured_logs
        }

    def f1e_get_build_log_full_content_tool(self, build_id: int, log_id: int) -> Dict[str, Any]:
        """
        LLM-friendly tool to retrieve full content of a specific build log.
        
        This tool retrieves the complete content of a specific log within a build.
        
        Parameters:
            build_id (int): The ID of the build
            log_id (int): The ID of the specific log to retrieve full content for
            
        Returns:
            Dict[str, Any]: A dictionary containing the full log content and metadata
        """
        try:
            log_content = self.build_client.get_build_log_lines(
                project=self.project, 
                build_id=build_id, 
                log_id=log_id
            )
            
            # Get log metadata
            logs = self.build_client.get_build_logs(project=self.project, build_id=build_id)
            log_metadata = None
            for log in logs:
                if log.id == log_id:
                    log_metadata = {
                        'id': log.id,
                        'type': log.type,
                        'url': log.url,
                        'createdOn': log.created_on.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if log.created_on else None,
                        'lastChangedOn': log.last_changed_on.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if log.last_changed_on else None,
                    }
                    break
            
            if not log_metadata:
                return {
                    'buildId': build_id,
                    'logId': log_id,
                    'error': f'Log with ID {log_id} not found in build {build_id}',
                    'content': []
                }
            
            return {
                'buildId': build_id,
                'logId': log_id,
                'logMetadata': log_metadata,
                'contentLines': log_content,
                'contentLineCount': len(log_content),
                'fullContent': '\n'.join(log_content)
            }
            
        except Exception as e:
            logging.error(f"Error retrieving full content for log {log_id} in build {build_id}: {e}")
            return {
                'buildId': build_id,
                'logId': log_id,
                'error': str(e),
                'content': []
            }
    
    def get_failed_tasks_with_logs(self, build_id: int) -> list:
        """
        Returns a list of failed tasks for a build, each with the last 200 lines of its log.
        Each item in the list is a dict with task name, log id, and last 200 log lines.
        """
        try:
            # Get build timeline (contains task results and log ids)
            timeline = self.build_client.get_build_timeline(project=self.project, build_id=build_id)
            if not timeline or not timeline.records:
                return []
            failed_tasks = []
            for record in timeline.records:
                if record.result == 'failed' and record.log and record.log.id:
                    log_id = record.log.id
                    log_lines = self.build_client.get_build_log_lines(
                        project=self.project,
                        build_id=build_id,
                        log_id=log_id
                    )
                    last_200 = log_lines[-200:] if len(log_lines) > 200 else log_lines
                    failed_tasks.append({
                        'taskName': record.name,
                        'logId': log_id,
                        'last200LogLines': last_200
                    })
            return failed_tasks
        except Exception as e:
            logging.error(f"Error retrieving failed tasks/logs for build {build_id}: {e}")
            return []

    def get_build_pipelines(self) -> List[Dict[str, Any]]:
        """
        Retrieve all build pipelines/definitions in the project.
        
        Returns:
            List of dictionaries containing build pipeline information
        """
        try:
            logging.info("Retrieving all build pipelines...")
            definitions = self.build_client.get_definitions(project=self.project)
            
            result = []
            for definition in definitions:
                try:
                    pipeline_info = {
                        'id': definition.id,
                        'name': definition.name,
                        'type': 'build',
                        'quality': 'definition',
                        'revision': getattr(definition, 'revision', 'Unknown'),
                        'createdDate': None,
                        'queueStatus': 'enabled',
                        'url': getattr(definition, 'url', 'Unknown'),
                        'path': getattr(definition, 'path', None),
                        'repository': None,
                        'authoredBy': None
                    }
                    result.append(pipeline_info)
                except Exception as e:
                    logging.error(f"Error processing definition {definition.id}: {e}")
                    continue
            
            logging.info(f"Found {len(result)} build pipelines.")
            return result
        except Exception as e:
            logging.error(f"Error retrieving build pipelines: {e}")
            return [{'error': str(e)}]

    def f1e_get_build_pipelines_tool(self) -> str:
        """
        LLM-friendly tool to retrieve all build pipelines/definitions.
        
        This tool retrieves all build pipelines in the project and formats them in a 
        human-readable string format suitable for LLM consumption.
        
        Returns:
            str: A formatted string with details about all build pipelines
        """
        pipelines = self.get_build_pipelines()
        
        if pipelines and 'error' in pipelines[0]:
            return f"Error retrieving build pipelines: {pipelines[0]['error']}"
        
        if not pipelines:
            return "No build pipelines found in the project."
        
        result = f"Found {len(pipelines)} build pipeline(s):\n\n"
        
        for pipeline in pipelines:
            result += f"Pipeline ID: {pipeline['id']}\n"
            result += f"Name: {pipeline['name']}\n"
            result += f"Type: {pipeline['type']}\n"
            result += f"Quality: {pipeline['quality']}\n"
            result += f"Revision: {pipeline['revision']}\n"
            result += f"Queue Status: {pipeline['queueStatus']}\n"
            
            if pipeline['path']:
                result += f"Path: {pipeline['path']}\n"
            
            if pipeline['createdDate']:
                result += f"Created: {pipeline['createdDate']}\n"
            
            if pipeline['authoredBy']:
                result += f"Authored by: {pipeline['authoredBy']['displayName']}\n"
            
            if pipeline['repository']:
                result += f"Repository: {pipeline['repository']['name']} ({pipeline['repository']['type']})\n"
            
            result += f"URL: {pipeline['url']}\n"
            result += "-" * 60 + "\n"
        
        return result
