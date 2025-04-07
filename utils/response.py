from rest_framework.response import Response
from rest_framework import status


NOT_FOUND_RESPONSE = Response({'detail':'존재하지 않는 항목입니다'}, status.HTTP_404_NOT_FOUND)

SUCCESS_RESPONSE = Response({'detail':'성공적으로 처리되었습니다'}, status.HTTP_200_OK)