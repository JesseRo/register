(function (card) {
    document.getElementsByName('ppw-accountHolderName')[0].value = card.name;
    document.getElementsByName('addCreditCardNumber')[0].value = card.number;
    document.getElementsByName('ppw-expirationDate_month')[0].value = card.month;
    document.getElementsByName('ppw-expirationDate_year')[0].value = card.year;
    document.getElementsByClassName('a-button-input')[0].click();
})(${card});