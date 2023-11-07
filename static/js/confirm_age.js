document.addEventListener('DOMContentLoaded', function () {
    var permissionBlock = document.querySelector('.permission-block');
    var overlay = document.querySelector('.overlay');
    var confirmButton = document.getElementById('confirmButton');
    if (document.cookie.indexOf('ConfirmAge=1') === -1) {
        permissionBlock.style.display = 'block';
        overlay.style.display = 'block';
    }
    confirmButton.addEventListener('click', function () {
        fetch('/confirm_age')
            .then(function (response) {
                if (response.ok) {
                    permissionBlock.style.display = 'none';
                    overlay.style.display = 'none';
                }
            })
            .catch(function (error) {
                console.log('Произошла ошибка:', error);
            });
    });
});
