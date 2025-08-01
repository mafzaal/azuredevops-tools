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
from azure.devops.v7_1.tfvc.models import TfvcChange,TfvcVersionDescriptor,TfvcChangesetSearchCriteria
from azure.devops.v7_1.build.models import Build
from azure.devops.v7_1.git.models import (
    GitPullRequest, GitPullRequestSearchCriteria,
    GitRepository, GitCommitRef, GitRefUpdate,
    GitPush, GitRepositoryRef, GitItem, GitCommit,
    IdentityRefWithVote
)

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
        self.git_client = self.connection.clients.get_git_client()
        self.policy_client = self.connection.clients.get_policy_client()
        self.work_item_tracking_client = self.connection.clients.get_work_item_tracking_client()
        self.core_client = self.connection.clients.get_core_client()

    def get_projects(self) -> List[Dict[str, Any]]:
        """
        Retrieve all projects from Azure DevOps organization.
        
        Returns:
            List of dictionaries containing project information including name, ID, state, and visibility
        """
        try:
            logging.info("Retrieving projects from Azure DevOps...")
            projects = self.core_client.get_projects()
            
            result = []
            for project in projects:
                result.append({
                    'id': project.id,
                    'name': project.name,
                    'description': project.description or '',
                    'state': project.state,
                    'visibility': project.visibility,
                    'url': project.url,
                    'lastUpdateTime': project.last_update_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if project.last_update_time else None
                })
            
            logging.info(f"Found {len(result)} projects.")
            return result
            
        except Exception as e:
            logging.error(f"Error retrieving projects: {e}")
            return []

    def get_changeset_list(self, author: Optional[str] = None, from_changeset_id: Optional[int] = None, to_changeset_id: Optional[int] = None, project: Optional[str] = None):
        """Retrieve changesets using azure-devops SDK."""
        project_name = project or self.project
        logging.info(f"Retrieving changesets since ID {from_changeset_id} for author {author}...")
        search_criteria = TfvcChangesetSearchCriteria()
        if author:
            search_criteria.author = author
        if from_changeset_id:
            search_criteria.from_id = from_changeset_id
        
        if to_changeset_id:
            search_criteria.to_id = to_changeset_id

        changesets = self.tfvc_client.get_changesets(
            project=project_name,
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
    
    def get_changeset(self, changeset_id, project: Optional[str] = None):
        """Retrieve a specific changeset by ID."""
        project_name = project or self.project
        try:
            changeset = self.tfvc_client.get_changeset(changeset_id, project=project_name)
            return {
                'changesetId': changeset.changeset_id,
                'comment': changeset.comment,
                'author': {'displayName': changeset.author.display_name if changeset.author else 'Unknown'},
                'createdDate': changeset.created_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if changeset.created_date else 'Unknown date'
            }
        except Exception as e:
            logging.error(f"Error retrieving changeset {changeset_id}: {e}")
            return None
    
    def get_changeset_changes(self, changeset_id, project: Optional[str] = None):
        """Get the files changed in a specific changeset."""
        project_name = project or self.project
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

    def get_file_content(self, file_path, changeset_id, version_option='None', project: Optional[str] = None):
        """Get content of a file at a specific changeset."""
        project_name = project or self.project
        try:
            version_descriptor= TfvcVersionDescriptor(str(changeset_id),version_option,'changeset')

            chunks = self.tfvc_client.get_item_content(
                path=file_path,
                version_descriptor=version_descriptor,
                project=project_name,
                download=True
            )

            
            content = ""
            for chunk in  chunks:
                content += chunk.decode('utf-8', errors='ignore')

            return content if content else ''

        except Exception as e:
            logging.error(f"Error retrieving content for {file_path} at changeset {changeset_id}: {e}")
            return ""

    def get_file_diff(self, file_path, changeset_id, project: Optional[str] = None):
        """Get diff of file changes in a specific changeset."""
        try:
            current_content = self.get_file_content(file_path, changeset_id, project=project)
            previous_content = self.get_file_content(file_path, changeset_id, version_option='Previous', project=project)
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

    def get_build(self, build_id: int, project: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve details about a specific build.
        
        Args:
            build_id: The ID of the build to retrieve
            project: Optional project name, defaults to instance project
            
        Returns:
            Dictionary containing build information including status and result
        """
        project_name = project or self.project
        try:
            logging.info(f"Retrieving build {build_id}...")
            build: Build = self.build_client.get_build(project=project_name, build_id=build_id)
            
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
            
    def get_builds(self, definition_id: Optional[int] = None, top: int = 50, status_filter: Optional[str] = None, project: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve multiple builds from the project.
        
        Args:
            definition_id: Optional definition ID to filter builds by specific pipeline
            top: Maximum number of builds to retrieve (default 50)
            status_filter: Optional status filter ('completed', 'inProgress', 'notStarted')
            project: Optional project name, defaults to instance project
            
        Returns:
            List of dictionaries containing build information
        """
        project_name = project or self.project
        try:
            logging.info(f"Retrieving up to {top} builds...")
            
            builds = self.build_client.get_builds(
                project=project_name,
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

    def get_build_logs(self, build_id: int, project: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve logs for a specific build.
        
        Args:
            build_id: The ID of the build to retrieve logs for
            project: Optional project name, defaults to instance project
            
        Returns:
            List of dictionaries containing log information and content
        """
        project_name = project or self.project
        try:
            logging.info(f"Retrieving logs for build {build_id}...")
            logs = self.build_client.get_build_logs(project=project_name, build_id=build_id)
            
            result = []
            for log in logs:
                log_content = self.build_client.get_build_log_lines(
                    project=project_name, 
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

    def f1e_get_build_tool(self, build_id: int, project: Optional[str] = None) -> str:
        """
        LLM-friendly tool to retrieve build status and details.
        
        This tool retrieves a specific build and formats the details in a human-readable string format
        that's suitable for LLM consumption.
        
        Parameters:
            build_id (int): The ID of the build to retrieve
            project (str, optional): Optional project name, defaults to instance project
            
        Returns:
            str: A formatted string with details about the build including status and result
        """
        build_info = self.get_build(build_id, project=project)
        
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
    
    def f1e_get_builds_tool(self, definition_id: Optional[int] = None, top: int = 50, status_filter: Optional[str] = None, project: Optional[str] = None) -> str:
        """
        LLM-friendly tool to retrieve multiple builds.
        
        This tool retrieves multiple builds and formats them in a human-readable string format
        suitable for LLM consumption.
        
        Parameters:
            definition_id (int, optional): Filter builds by specific pipeline/definition ID
            top (int): Maximum number of builds to retrieve (default 50)
            status_filter (str, optional): Filter by status ('completed', 'inProgress', 'notStarted')
            project (str, optional): Optional project name, defaults to instance project
            
        Returns:
            str: A formatted string with details about multiple builds
        """
        builds = self.get_builds(definition_id, top, status_filter, project=project)
        
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

    def f1e_get_build_logs_tool(self, build_id: int, project: Optional[str] = None) -> Dict[str, Any]:
        """
        LLM-friendly tool to retrieve build logs summary with last 50 lines of content.

        This tool retrieves logs for a specific build and returns them as a structured
        dictionary object with metadata and last 50 lines of content for each log.

        Parameters:
            build_id (int): The ID of the build to retrieve logs for
            project (str, optional): Optional project name, defaults to instance project

        Returns:
            Dict[str, Any]: A dictionary containing build logs with metadata and preview content
        """
        logs = self.get_build_logs(build_id, project=project)

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

    def f1e_get_build_log_full_content_tool(self, build_id: int, log_id: int, project: Optional[str] = None) -> Dict[str, Any]:
        """
        LLM-friendly tool to retrieve full content of a specific build log.
        
        This tool retrieves the complete content of a specific log within a build.
        
        Parameters:
            build_id (int): The ID of the build
            log_id (int): The ID of the specific log to retrieve full content for
            project (str, optional): Optional project name, defaults to instance project
            
        Returns:
            Dict[str, Any]: A dictionary containing the full log content and metadata
        """
        project_name = project or self.project
        try:
            log_content = self.build_client.get_build_log_lines(
                project=project_name, 
                build_id=build_id, 
                log_id=log_id
            )
            
            # Get log metadata
            logs = self.build_client.get_build_logs(project=project_name, build_id=build_id)
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
    
    def get_failed_tasks_with_logs(self, build_id: int, project: Optional[str] = None) -> list:
        """
        Returns a list of failed tasks for a build, each with the last 200 lines of its log.
        Each item in the list is a dict with task name, log id, and last 200 log lines.
        """
        project_name = project or self.project
        try:
            # Get build timeline (contains task results and log ids)
            timeline = self.build_client.get_build_timeline(project=project_name, build_id=build_id)
            if not timeline or not timeline.records:
                return []
            failed_tasks = []
            for record in timeline.records:
                if record.result == 'failed' and record.log and record.log.id:
                    log_id = record.log.id
                    log_lines = self.build_client.get_build_log_lines(
                        project=project_name,
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

    def get_build_pipelines(self, project: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve all build pipelines/definitions in the project.
        
        Args:
            project: Optional project name, defaults to instance project
        
        Returns:
            List of dictionaries containing build pipeline information
        """
        project_name = project or self.project
        try:
            logging.info("Retrieving all build pipelines...")
            definitions = self.build_client.get_definitions(project=project_name)
            
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

    def f1e_get_build_pipelines_tool(self, project: Optional[str] = None) -> str:
        """
        LLM-friendly tool to retrieve all build pipelines/definitions.
        
        This tool retrieves all build pipelines in the project and formats them in a 
        human-readable string format suitable for LLM consumption.
        
        Parameters:
            project (str, optional): Optional project name, defaults to instance project
        
        Returns:
            str: A formatted string with details about all build pipelines
        """
        pipelines = self.get_build_pipelines(project=project)
        
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

    # Git Repository Operations
    def get_git_repositories(self, project: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all Git repositories in the project.
        
        Parameters:
            project (str, optional): The project name. If not provided, uses default project.
            
        Returns:
            List[Dict[str, Any]]: List of repository information dictionaries.
        """
        project_name = project or self.project
        logging.info(f"Retrieving Git repositories for project {project_name}...")
        
        try:
            repositories = self.git_client.get_repositories(project=project_name)
            
            repo_list = []
            for repo in repositories:
                repo_dict = {
                    'id': repo.id,
                    'name': repo.name,
                    'url': repo.url,
                    'defaultBranch': repo.default_branch,
                    'size': repo.size,
                    'remoteUrl': repo.remote_url,
                    'sshUrl': repo.ssh_url,
                    'webUrl': repo.web_url,
                    'isDisabled': repo.is_disabled,
                    'isFork': repo.is_fork,
                    'projectId': repo.project.id if repo.project else None,
                    'projectName': repo.project.name if repo.project else None
                }
                repo_list.append(repo_dict)
            
            return repo_list
            
        except Exception as e:
            logging.error(f"Error retrieving Git repositories: {e}")
            return []

    def get_git_repository(self, repository_id: str, project: Optional[str] = None) -> Dict[str, Any]:
        """
        Get details of a specific Git repository.
        
        Parameters:
            repository_id (str): The repository ID or name.
            project (str, optional): The project name. If not provided, uses default project.
            
        Returns:
            Dict[str, Any]: Repository information dictionary.
        """
        project_name = project or self.project
        logging.info(f"Retrieving Git repository {repository_id} from project {project_name}...")
        
        try:
            repository = self.git_client.get_repository(project=project_name, repository_id=repository_id)
            
            return {
                'id': repository.id,
                'name': repository.name,
                'url': repository.url,
                'defaultBranch': repository.default_branch,
                'size': repository.size,
                'remoteUrl': repository.remote_url,
                'sshUrl': repository.ssh_url,
                'webUrl': repository.web_url,
                'isDisabled': repository.is_disabled,
                'isFork': repository.is_fork,
                'projectId': repository.project.id if repository.project else None,
                'projectName': repository.project.name if repository.project else None
            }
            
        except Exception as e:
            logging.error(f"Error retrieving Git repository {repository_id}: {e}")
            return {}

    def get_git_commits(self, repository_id: str, branch: Optional[str] = None, top: int = 50, 
                       skip: int = 0, project: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get Git commits from a repository.
        
        Parameters:
            repository_id (str): The repository ID or name.
            branch (str, optional): The branch name. If not provided, uses default branch.
            top (int): Maximum number of commits to retrieve.
            skip (int): Number of commits to skip.
            project (str, optional): The project name. If not provided, uses default project.
            
        Returns:
            List[Dict[str, Any]]: List of commit information dictionaries.
        """
        project_name = project or self.project
        logging.info(f"Retrieving Git commits from repository {repository_id}...")
        
        try:
            # Create search criteria - this is required for the get_commits method
            from azure.devops.v7_0.git.models import GitQueryCommitsCriteria
            
            search_criteria = GitQueryCommitsCriteria()
            search_criteria.skip = skip
            search_criteria.top = top
            
            # Set branch if provided
            if branch:
                search_criteria.item_version = {
                    'version': branch,
                    'version_type': 'branch'
                }
            
            commits = self.git_client.get_commits(
                repository_id=repository_id,
                search_criteria=search_criteria,
                project=project_name
            )
            
            commit_list = []
            for commit in commits:
                commit_dict = {
                    'commitId': commit.commit_id,
                    
                    'branch': commit.branch.name if commit.branch else None,
                    'comment': commit.comment,
                    'author': {
                        'name': commit.author.name,
                        'email': commit.author.email,
                        'date': commit.author.date.isoformat() if commit.author.date else None
                    } if commit.author else None,
                    'committer': {
                        'name': commit.committer.name,
                        'email': commit.committer.email,
                        'date': commit.committer.date.isoformat() if commit.committer.date else None
                    } if commit.committer else None,
                    'changeCounts': commit.change_counts,
                    'url': commit.url,
                    'remoteUrl': commit.remote_url
                }
                commit_list.append(commit_dict)
            
            return commit_list
            
        except Exception as e:
            error_msg = f"Error retrieving Git commits from repository {repository_id}: {str(e)}"
            logging.error(error_msg)
            # Return more detailed error information for LLM-friendly tools
            return [{
                'error': True,
                'error_message': str(e),
                'error_details': f"Failed to retrieve commits from repository '{repository_id}' in project '{project_name}'",
                'repository_id': repository_id,
                'project': project_name
            }]

    def get_git_commit_details(self, repository_id: str, commit_id: str, 
                              project: Optional[str] = None) -> Dict[str, Any]:
        """
        Get detailed information about a specific Git commit.
        
        Parameters:
            repository_id (str): The repository ID or name.
            commit_id (str): The commit SHA (can be abbreviated).
            project (str, optional): The project name. If not provided, uses default project.
            
        Returns:
            Dict[str, Any]: Detailed commit information.
        """
        project_name = project or self.project
        logging.info(f"Retrieving Git commit details for {commit_id} from repository {repository_id}...")
        
        try:
            # If the commit ID is not a full SHA, search for it
            # if len(commit_id) < 40:
            #     logging.info(f"Commit ID {commit_id} is abbreviated, searching for full SHA...")
            #     from azure.devops.v7_0.git.models import GitQueryCommitsCriteria
            #     search_criteria = GitQueryCommitsCriteria(ids=commit_id)
            #     commits = self.git_client.get_commits(
            #         repository_id=repository_id,
            #         search_criteria=search_criteria,
            #         project=project_name
            #     )
            #     if commits:
            #         commit_id = commits[0].commit_id
            #         logging.info(f"Found full commit SHA: {commit_id}")
            #     else:
            #         logging.error(f"Could not find full commit SHA for {commit_id}")
            #         return {}

            commit = self.git_client.get_changes(
                repository_id=repository_id,
                commit_id=commit_id,
                project=project_name
            )
            
            # Get commit changes
            # changes = self.git_client.get_changes(
            #     repository_id=repository_id,
            #     commit_id=commit_id,
            #     project=project_name
            # ).changes
            
            # change_list = []
            # for change in changes:
            #     change_dict = {
            #         'changeType': str(change.change_type),
            #         'item': {
            #             'path': change.item.path if change.item else None,
            #             'gitObjectType': str(change.item.git_object_type) if change.item else None
            #         }
            #     }
            #     change_list.append(change_dict)
            
            return {
                'commitId': commit.commit_id,
                'comment': commit.comment,
                'author': {
                    'name': commit.author.name,
                    'email': commit.author.email,
                    'date': commit.author.date.isoformat() if commit.author.date else None
                } if commit.author else None,
                'committer': {
                    'name': commit.committer.name,
                    'email': commit.committer.email,
                    'date': commit.committer.date.isoformat() if commit.committer.date else None
                } if commit.committer else None,
                'changeCounts': commit.change_counts,
                'url': commit.url,
                'remoteUrl': commit.remote_url,
                # 'changes': change_list
            }
            
        except Exception as e:
            logging.error(f"Error retrieving Git commit details for {commit_id}: {e}")
            return {}

    # Pull Request Operations
    def get_pull_requests(self, repository_id: str, status: str = 'active', 
                         target_branch: Optional[str] = None, source_branch: Optional[str] = None,
                         creator: Optional[str] = None, reviewer: Optional[str] = None,
                         top: int = 50, project: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get pull requests from a Git repository.
        
        Parameters:
            repository_id (str): The repository ID or name.
            status (str): PR status ('active', 'completed', 'abandoned', 'all').
            target_branch (str, optional): Filter by target branch.
            source_branch (str, optional): Filter by source branch.
            creator (str, optional): Filter by creator.
            reviewer (str, optional): Filter by reviewer.
            top (int): Maximum number of PRs to retrieve.
            project (str, optional): The project name. If not provided, uses default project.
            
        Returns:
            List[Dict[str, Any]]: List of pull request information dictionaries.
        """
        project_name = project or self.project
        logging.info(f"Retrieving pull requests from repository {repository_id}...")
        
        try:
            search_criteria = GitPullRequestSearchCriteria()
            
            if status != 'all':
                if status == 'active':
                    search_criteria.status = 'active'
                elif status == 'completed':
                    search_criteria.status = 'completed'
                elif status == 'abandoned':
                    search_criteria.status = 'abandoned'
            
            if target_branch:
                search_criteria.target_ref_name = f"refs/heads/{target_branch}"
            if source_branch:
                search_criteria.source_ref_name = f"refs/heads/{source_branch}"
            if creator:
                search_criteria.creator_id = creator
            if reviewer:
                search_criteria.reviewer_id = reviewer
            
            pull_requests = self.git_client.get_pull_requests(
                repository_id=repository_id,
                search_criteria=search_criteria,
                project=project_name,
                top=top
            )
            
            pr_list = []
            for pr in pull_requests:
                pr_dict = {
                    'pullRequestId': pr.pull_request_id,
                    'title': pr.title,
                    'description': pr.description,
                    'status': str(pr.status),
                    'createdBy': {
                        'displayName': pr.created_by.display_name,
                        'uniqueName': pr.created_by.unique_name,
                        'id': pr.created_by.id
                    } if pr.created_by else None,
                    'creationDate': pr.creation_date.isoformat() if pr.creation_date else None,
                    'closedDate': pr.closed_date.isoformat() if pr.closed_date else None,
                    'sourceRefName': pr.source_ref_name,
                    'targetRefName': pr.target_ref_name,
                    'lastMergeSourceCommit': pr.last_merge_source_commit.commit_id if pr.last_merge_source_commit else None,
                    'lastMergeTargetCommit': pr.last_merge_target_commit.commit_id if pr.last_merge_target_commit else None,
                    'isDraft': pr.is_draft,
                    'mergeStatus': str(pr.merge_status) if pr.merge_status else None,
                    'url': pr.url,
                    'reviewers': [
                        {
                            'displayName': reviewer.display_name,
                            'uniqueName': reviewer.unique_name,
                            'id': reviewer.id,
                            'vote': reviewer.vote,
                            'isRequired': reviewer.is_required,
                            'isFlagged': reviewer.is_flagged
                        } for reviewer in pr.reviewers
                    ] if pr.reviewers else []
                }
                pr_list.append(pr_dict)
            
            return pr_list
            
        except Exception as e:
            logging.error(f"Error retrieving pull requests from repository {repository_id}: {e}")
            return []

    def get_pull_request_details(self, repository_id: str, pull_request_id: int, 
                                project: Optional[str] = None) -> Dict[str, Any]:
        """
        Get detailed information about a specific pull request.
        
        Parameters:
            repository_id (str): The repository ID or name.
            pull_request_id (int): The pull request ID.
            project (str, optional): The project name. If not provided, uses default project.
            
        Returns:
            Dict[str, Any]: Detailed pull request information.
        """
        project_name = project or self.project
        logging.info(f"Retrieving pull request details for PR {pull_request_id}...")
        
        try:
            pr = self.git_client.get_pull_request(
                repository_id=repository_id,
                pull_request_id=pull_request_id,
                project=project_name
            )
            
            # Get work items linked to PR
            work_items = []
            try:
                work_item_refs = self.git_client.get_pull_request_work_item_refs(
                    repository_id=repository_id,
                    pull_request_id=pull_request_id,
                    project=project_name
                )
                for wi_ref in work_item_refs:
                    work_items.append({
                        'id': wi_ref.id,
                        'url': wi_ref.url
                    })
            except:
                pass  # Work items might not be available
            
            return {
                'pullRequestId': pr.pull_request_id,
                'title': pr.title,
                'description': pr.description,
                'status': str(pr.status),
                'createdBy': {
                    'displayName': pr.created_by.display_name,
                    'uniqueName': pr.created_by.unique_name,
                    'id': pr.created_by.id
                } if pr.created_by else None,
                'creationDate': pr.creation_date.isoformat() if pr.creation_date else None,
                'closedDate': pr.closed_date.isoformat() if pr.closed_date else None,
                'closedBy': {
                    'displayName': pr.closed_by.display_name,
                    'uniqueName': pr.closed_by.unique_name,
                    'id': pr.closed_by.id
                } if pr.closed_by else None,
                'sourceRefName': pr.source_ref_name,
                'targetRefName': pr.target_ref_name,
                'lastMergeSourceCommit': pr.last_merge_source_commit.commit_id if pr.last_merge_source_commit else None,
                'lastMergeTargetCommit': pr.last_merge_target_commit.commit_id if pr.last_merge_target_commit else None,
                'isDraft': pr.is_draft,
                'mergeStatus': str(pr.merge_status) if pr.merge_status else None,
                'url': pr.url,
                'reviewers': [
                    {
                        'displayName': reviewer.display_name,
                        'uniqueName': reviewer.unique_name,
                        'id': reviewer.id,
                        'vote': reviewer.vote,
                        'isRequired': reviewer.is_required,
                        'isFlagged': reviewer.is_flagged,
                        'hasDeclined': reviewer.has_declined
                    } for reviewer in pr.reviewers
                ] if pr.reviewers else [],
                'workItemRefs': work_items,
                'labels': [label.name for label in pr.labels] if pr.labels else [],
                'completionOptions': pr.completion_options,
                'completionQueueTime': pr.completion_queue_time.isoformat() if pr.completion_queue_time else None
            }
            
        except Exception as e:
            logging.error(f"Error retrieving pull request details for PR {pull_request_id}: {e}")
            return {}

    def create_pull_request(self, repository_id: str, title: str, description: str,
                           source_branch: str, target_branch: str, 
                           reviewers: Optional[List[str]] = None, work_items: Optional[List[int]] = None,
                           is_draft: bool = False, project: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new pull request.
        
        Parameters:
            repository_id (str): The repository ID or name.
            title (str): The pull request title.
            description (str): The pull request description.
            source_branch (str): The source branch name.
            target_branch (str): The target branch name.
            reviewers (List[str], optional): List of reviewer IDs or emails.
            work_items (List[int], optional): List of work item IDs to link.
            is_draft (bool): Whether to create as draft PR.
            project (str, optional): The project name. If not provided, uses default project.
            
        Returns:
            Dict[str, Any]: Created pull request information.
        """
        project_name = project or self.project
        logging.info(f"Creating pull request from {source_branch} to {target_branch}...")
        
        try:
            # Create the pull request object
            pr = GitPullRequest()
            pr.title = title
            pr.description = description
            pr.source_ref_name = f"refs/heads/{source_branch}"
            pr.target_ref_name = f"refs/heads/{target_branch}"
            pr.is_draft = is_draft
            
            # Add reviewers if provided
            if reviewers:
                pr.reviewers = []
                for reviewer_id in reviewers:
                    reviewer = IdentityRefWithVote()
                    reviewer.id = reviewer_id
                    pr.reviewers.append(reviewer)
            
            # Create the pull request
            created_pr = self.git_client.create_pull_request(
                git_pull_request_to_create=pr,
                repository_id=repository_id,
                project=project_name
            )
            
            return {
                'pullRequestId': created_pr.pull_request_id,
                'title': created_pr.title,
                'description': created_pr.description,
                'status': str(created_pr.status),
                'createdBy': {
                    'displayName': created_pr.created_by.display_name,
                    'uniqueName': created_pr.created_by.unique_name,
                    'id': created_pr.created_by.id
                } if created_pr.created_by else None,
                'creationDate': created_pr.creation_date.isoformat() if created_pr.creation_date else None,
                'sourceRefName': created_pr.source_ref_name,
                'targetRefName': created_pr.target_ref_name,
                'isDraft': created_pr.is_draft,
                'url': created_pr.url
            }
            
        except Exception as e:
            logging.error(f"Error creating pull request: {e}")
            return {'error': str(e)}

    def update_pull_request_vote(self, repository_id: str, pull_request_id: int,
                                reviewer_id: str, vote: int, project: Optional[str] = None) -> Dict[str, Any]:
        """
        Update a reviewer's vote on a pull request.
        
        Parameters:
            repository_id (str): The repository ID or name.
            pull_request_id (int): The pull request ID.
            reviewer_id (str): The reviewer's ID.
            vote (int): The vote (-10: rejected, -5: waiting for author, 0: no vote, 5: approved with suggestions, 10: approved).
            project (str, optional): The project name. If not provided, uses default project.
            
        Returns:
            Dict[str, Any]: Updated reviewer information.
        """
        project_name = project or self.project
        logging.info(f"Updating vote for PR {pull_request_id} by reviewer {reviewer_id}...")
        
        try:
            reviewer = IdentityRefWithVote()
            reviewer.id = reviewer_id
            reviewer.vote = vote
            
            updated_reviewer = self.git_client.create_pull_request_reviewer(
                reviewer=reviewer,
                repository_id=repository_id,
                pull_request_id=pull_request_id,
                reviewer_id=reviewer_id,
                project=project_name
            )
            
            vote_description = {
                -10: "Rejected",
                -5: "Waiting for Author", 
                0: "No Vote",
                5: "Approved with Suggestions",
                10: "Approved"
            }.get(vote, "Unknown")
            
            return {
                'reviewerId': updated_reviewer.id,
                'displayName': updated_reviewer.display_name,
                'vote': updated_reviewer.vote,
                'voteDescription': vote_description,
                'isRequired': updated_reviewer.is_required,
                'isFlagged': updated_reviewer.is_flagged
            }
            
        except Exception as e:
            logging.error(f"Error updating vote for PR {pull_request_id}: {e}")
            return {'error': str(e)}

    def get_pull_request_policies(self, repository_id: str, pull_request_id: int, 
                                 project: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get branch policies that apply to a pull request.
        
        Parameters:
            repository_id (str): The repository ID or name.
            pull_request_id (int): The pull request ID.
            project (str, optional): The project name. If not provided, uses default project.
            
        Returns:
            List[Dict[str, Any]]: List of policy evaluation records.
        """
        project_name = project or self.project
        logging.info(f"Retrieving policies for PR {pull_request_id}...")
        
        try:
            # Get PR details first to get artifact ID
            pr = self.git_client.get_pull_request(
                repository_id=repository_id,
                pull_request_id=pull_request_id,
                project=project_name
            )
            
            # Get policy evaluations
            artifact_id = f"vstfs:///CodeReview/CodeReviewId/{project_name}/{pull_request_id}"
            
            policy_evaluations = self.policy_client.get_policy_evaluations(
                project=project_name,
                artifact_id=artifact_id
            )
            
            policy_list = []
            for evaluation in policy_evaluations:
                policy_dict = {
                    'evaluationId': evaluation.evaluation_id,
                    'status': str(evaluation.status),
                    'policyId': evaluation.policy_id,
                    'startedDate': evaluation.started_date.isoformat() if evaluation.started_date else None,
                    'completedDate': evaluation.completed_date.isoformat() if evaluation.completed_date else None,
                    'context': evaluation.context,
                    'configuration': evaluation.configuration
                }
                policy_list.append(policy_dict)
            
            return policy_list
            
        except Exception as e:
            logging.error(f"Error retrieving policies for PR {pull_request_id}: {e}")
            return []

    def f1e_get_git_commits_tool(self, repository_id: str, branch: Optional[str] = None, 
                                top: int = 10, project: Optional[str] = None) -> str:
        """
        LLM-friendly tool to retrieve Git commits from a repository.
        
        This tool retrieves recent commits from a Git repository and formats them in a 
        human-readable string format suitable for LLM consumption, with enhanced error handling.
        
        Parameters:
            repository_id (str): The repository ID or name.
            branch (str, optional): The branch name. If not provided, uses default branch.
            top (int): Maximum number of commits to retrieve (default: 10).
            project (str, optional): The project name. If not provided, uses default project.
            
        Returns:
            str: A formatted string with commit details or error information.
        """
        commits = self.get_git_commits(repository_id, branch=branch, top=top, project=project)
        
        # Check for error in response
        if commits and len(commits) == 1 and isinstance(commits[0], dict) and commits[0].get('error'):
            error_info = commits[0]
            return f"Error retrieving Git commits from repository '{repository_id}':\n\n" \
                   f"Error: {error_info['error_message']}\n" \
                   f"Details: {error_info['error_details']}\n" \
                   f"Repository: {error_info['repository_id']}\n" \
                   f"Project: {error_info['project']}"
        
        if not commits:
            return f"No commits found in repository '{repository_id}'" + \
                   (f" on branch '{branch}'" if branch else "") + \
                   f" in project '{project or self.project}'"
        
        result = f"Found {len(commits)} commits from repository {repository_id}"
        if branch:
            result += f" on branch '{branch}'"
        result += f" in project '{project or self.project}':\n\n"
        
        for commit in commits:
            result += f"Commit: {commit['commitId'][:12]}..."
            if commit.get('author') and commit['author'].get('date'):
                result += f" ({commit['author']['date']})"
            result += "\n"
            
            if commit.get('author'):
                result += f"Author: {commit['author'].get('name', 'Unknown')}"
                if commit['author'].get('email'):
                    result += f" <{commit['author']['email']}>"
                result += "\n"
            
            if commit.get('comment'):
                # Truncate long commit messages for readability
                comment = commit['comment'].strip()
                if len(comment) > 100:
                    comment = comment[:97] + "..."
                result += f"Message: {comment}\n"
            
            if commit.get('changeCounts'):
                try:
                    changes = commit['changeCounts']
                    if isinstance(changes, dict):
                        adds = changes.get('Add', 0)
                        edits = changes.get('Edit', 0) 
                        deletes = changes.get('Delete', 0)
                        total = adds + edits + deletes
                        result += f"Changes: +{adds} ~{edits} -{deletes} ({total} total)\n"
                except (TypeError, AttributeError):
                    pass
            
            if commit.get('url'):
                result += f"URL: {commit['url']}\n"
            
            result += "-" * 60 + "\n"
        
        return result
