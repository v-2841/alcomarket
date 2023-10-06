document.addEventListener('DOMContentLoaded', function() {
    var addToCartButtons = document.querySelectorAll('.add-to-cart-button');
    addToCartButtons.forEach(function(addToCartButton) {
        var goodId = addToCartButton.getAttribute('data-good-id');
        checkCartStatus(goodId, addToCartButton);
        addToCartButton.addEventListener('click', function() {
            var url = '/' + goodId + '/add/';
            if (addToCartButton.textContent === 'Добавлено') {
                url = '/' + goodId + '/remove/';
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
                    if (addToCartButton.textContent === 'Добавлено') {
                        addToCartButton.textContent = 'В корзину';
                    } else {
                        addToCartButton.textContent = 'Добавлено';
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
    function checkCartStatus(goodId, addToCartButton) {
        var url = '/' + goodId + '/check/';
        fetch(url)
        .then(response => {
            if (response.status === 200) {
                return response.json();
            } else {
                console.error('Ошибка при проверке корзины');
            }
        })
        .then(data => {
            if (data.is_in_cart) {
                addToCartButton.textContent = 'Добавлено';
            }
            else addToCartButton.textContent = 'В корзину';
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
    }
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
