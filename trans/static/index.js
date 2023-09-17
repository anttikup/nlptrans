window.Trans = {};

const isValidValue = selected => {
    const options = document.querySelectorAll('option');
    for (const option of options) {
        if ( option.textContent.trim() === selected ) {
            return true;
        }
    }
    return false;
};

const validateLanguageBox = () => {
    const selected = document.forms["translate"]["language"].value;

    if ( isValidValue(selected) ) {
        document.forms["translate"]["language"].setCustomValidity('');
    } else {
        document.forms["translate"]["language"].setCustomValidity('Virheellinen mallin nimi');
    }
}

document.querySelector('[name="language"]').addEventListener('input', event => {
    validateLanguageBox();
});

document.querySelector('form').addEventListener('submit', event => {
    document.querySelectorAll('.flash').forEach(node => node.remove());

    if ( document.forms["translate"]["language"].checkValidity() ) {
        return true;
    }

    return false;
});


validateLanguageBox();

jQuery( function () {
    const input = new Trans.ModelLookupTextInputWidget( {
        icon: 'language'
    } );

    const value = $('[name="language"]').val();
    input.setValue(value);
    input.$element.find('input').attr('name', 'language');

    $( '[name="language"]' ).replaceWith(
	input.$element
    );


} );
