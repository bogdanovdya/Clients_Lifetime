%from bitrix24.bitrix24 import Bitrix24
<h1>Index Page</h1>
<%
bx24 = bitrix24.Bitrix24('YOUR_THIRD_LEVEL_DOMAIN', 'YOUR_AUTH_TOKEN')
print(bx24.call('app.info'))
        %>