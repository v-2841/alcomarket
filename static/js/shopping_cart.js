document.addEventListener('DOMContentLoaded', function() {
    var addToCartButtons = document.querySelectorAll('.add-to-cart-button');
    addToCartButtons.forEach(function(addToCartButton) {
        var goodId = addToCartButton.getAttribute('data-good-id');
        addToCartButton.addEventListener('click', function() {
            var url = '/goods/' + goodId + '/add/';
            if (addToCartButton.textContent.includes('Добавлено')) {
                url = '/goods/' + goodId + '/remove/';
            }
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({'action': 'toggle'}),
            })
            .then(response => {
                if (response.status === 200) {
                    if (addToCartButton.textContent.includes('Добавлено')) {
                        addToCartButton.textContent = 'В корзину';
                        addToCartButton.classList.remove('btn-green');
                        addToCartButton.classList.add('btn-pink');
                    } else {
                        addToCartButton.textContent = 'Добавлено';
                        addToCartButton.classList.remove('btn-pink');
                        addToCartButton.classList.add('btn-green');
                    }
                } else {
                    console.error('Ошибка при обновлении корзины');
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
            });
        });
    });
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
