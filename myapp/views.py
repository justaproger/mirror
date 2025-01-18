from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from revproxy.views import ProxyView

@method_decorator(login_required, name='dispatch')
class MyProxyView(ProxyView):
    upstream = 'https://student.tdau.uz'

    def add_custom_script(self, content):
        try:
            decoded_content = content.decode('utf-8')
            script = '''
            <script>
            document.addEventListener('keydown', function(event) {
                if (event.ctrlKey && event.code === 'Space') {
                    navigator.clipboard.readText().then(text => {
                        if (text) {
                            var encodedQuestion = encodeURIComponent(text);
                            var url = 'https://flask-production-42ee8.up.railway.app/' + encodedQuestion;

                            fetch(url)
                            .then(response => response.json())
                            .then(data => {
                                alert(data.answer);
                            })
                            .catch(error => {
                                console.error('Error:', error);
                            });
                        } else {
                            alert('Буфер обмена пуст.');
                        }
                    }).catch(err => {
                        console.error('Ошибка при чтении из буфера обмена: ', err);
                        alert('Ошибка при чтении из буфера обмена.');
                    });
                }
            });
            </script>
            '''
            return decoded_content.replace('</body>', script + '</body>').encode('utf-8')
        except UnicodeDecodeError:
            return content

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if response.streaming:
            response.streaming_content = (self.add_custom_script(chunk) for chunk in response.streaming_content)
        else:
            response.content = self.add_custom_script(response.content)
        return response