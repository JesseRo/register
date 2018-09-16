(function (card) {
    document.getElementById('pp-rO-40').value = card.name;
    document.getElementById('pp-rO-41').value = card.number;
    document.getElementById('pp-rO-43').value = card.month;
    document.getElementById('pp-rO-45').value = card.year;
    document.getElementsByClassName('a-button-input')[0].click();
})(${card});