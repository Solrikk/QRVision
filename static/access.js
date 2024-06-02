document.getElementById('submitCode').addEventListener('click', () => {
    const accessCode = document.getElementById('accessCode').value;
    if (accessCode === '1111') {
        window.location.href = '/operator';
    } else if (accessCode === '2222') {
        window.location.href = '/admin';
    } else {
        alert('Неверный код доступа');
    }
});