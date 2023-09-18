window.Trans = {};

const addError = (msg) => {
    const $flash = $('<div class="flash"></div>');
    $flash.text(msg);
    $('header').after($flash);
};

const setCookie = (cname, cvalue, exdays) => {
    const d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    const expires = "expires=" + d.toUTCString();
    document.cookie = [
        cname + "=" + cvalue,
        expires,
        "path=/",
        "SameSite=Strict"
    ].join(";");
};

const getCookie = (cname) => {
    const name = cname + "=";
    const decodedCookie = decodeURIComponent(document.cookie);
    const ca = decodedCookie.split(';');
    for ( let i = 0; i < ca.length; i++ ) {
        let c = ca[i];
        while ( c.charAt(0) == ' ' ) {
            c = c.substring(1);
        }
        if ( c.indexOf(name) == 0 ) {
            return c.substring(name.length, c.length);
        }
    }
    return null;
};

jQuery( function () {
    const modelInput = new Trans.ModelLookupTextInputWidget( {
        icon: 'language',
        id: 'language',
        value: getCookie('language') || 'englanti - suomi'
    } );
    const textToTranslate = new OO.ui.MultilineTextInputWidget( {
        value: '',
        rows: 20,
        id: 'text'
    } );
    const button = new OO.ui.ButtonInputWidget( {
        label: 'Käännä',
        title: 'Käännä teksti',
        icon: 'translate',
        flags: 'progressive',
    } );
    const translatedText = new OO.ui.MultilineTextInputWidget( {
        value: '',
        id: 'translation'
    } );

    const form = new OO.ui.FormLayout( {
        items: [
            new OO.ui.FieldLayout( modelInput, {
                label: 'Malli',
                align: 'top'
            } ),
            new OO.ui.FieldLayout( textToTranslate, {
                label: 'Teksti',
                align: 'top'
            } ),
            new OO.ui.FieldLayout( button, {
            } ),
        ],
    } )

    const form2 = new OO.ui.FormLayout( {
        id: 'form2',
        items: [
            new OO.ui.FieldLayout( translatedText, {
                label: 'Käännös',
                align: 'top'
            } ),
        ],
    } )

    $( '.grid' ).append( form.$element );
    $( '.grid' ).append( form2.$element );

    button.on('click', () => {
        const language = modelInput.getValue();
        const text = textToTranslate.getValue();
        setCookie('language', language, 7);

        $('#translation').addClass('loading');
        translatedText.setValue('');

        document.querySelectorAll('.flash').forEach(node => node.remove());

        $.post( 'translate', { text, language }, data => {
            if ( data.error ) {
                addError(data.error);
            } else {
                translatedText.setValue(data.text);
            }
            $('#translation').removeClass('loading');
        }).fail(error => {
            addError('Palvelinvirhe');
        });
    });

} );
