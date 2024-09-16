from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .github_service import (
    list_repositories,
    invite_collaborator,
    remove_collaborator,
    revoke_all_access,
    GitHubAPIError
)


class ListRepositories(APIView):
    def get(self, request):
        try:
            repos = list_repositories()
            return Response(repos, status=status.HTTP_200_OK)
        except GitHubAPIError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class InviteCollaborator(APIView):
    def post(self, request):
        try:
            repo_name = request.data.get('repo')
            username = request.data.get('username')
            permission = request.data.get('permission', 'push')

            if not repo_name or not username:
                return Response({"error": "Repository name and username are required"},
                                status=status.HTTP_400_BAD_REQUEST)

            owner = 'Babar-developer'  # You should replace this with logic to determine the owner dynamically if needed
            response = invite_collaborator(owner, repo_name, username, permission)
            return Response(response, status=status.HTTP_201_CREATED)
        except GitHubAPIError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RemoveCollaborator(APIView):
    def post(self, request):
        try:
            repo_name = request.data.get('repo')
            username = request.data.get('username')
            owner = 'Babar-developer'  # Adjust as needed

            if not repo_name or not username:
                return Response({"error": "Repository name and username are required"},
                                status=status.HTTP_400_BAD_REQUEST)

            result = remove_collaborator(owner, repo_name, username)
            return Response(result, status=status.HTTP_204_NO_CONTENT)
        except GitHubAPIError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RevokeAllAccess(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            if not username:
                return Response({"error": "Username is required"},
                                status=status.HTTP_400_BAD_REQUEST)

            result = revoke_all_access(username)
            return Response(result, status=status.HTTP_200_OK)
        except GitHubAPIError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
