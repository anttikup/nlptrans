/**
 * Trans for LookupElement.
 *
 * @class
 * @extends OO.ui.TextInputWidget
 * @mixins OO.ui.mixin.LookupElement
 *
 * @constructor
 * @param {Object} config Configuration options
 */
Trans.ModelLookupTextInputWidget = function TransModelLookupTextInputWidget( config ) {
    // Parent constructor
    OO.ui.TextInputWidget.call( this, $.extend( { validate: 'string' }, config ) );
    // Mixin constructors
    OO.ui.mixin.LookupElement.call( this, { ...config, allowSuggestionsWhenEmpty: true } );
};
OO.inheritClass( Trans.ModelLookupTextInputWidget, OO.ui.TextInputWidget );
OO.mixinClass( Trans.ModelLookupTextInputWidget, OO.ui.mixin.LookupElement );

/**
 * @inheritdoc
 */
Trans.ModelLookupTextInputWidget.prototype.getLookupRequest = function () {
    const value = this.getValue(),
          deferred = $.Deferred();

    this.getValidity().then( function () {
        $.getJSON('lookup', { 'text': value }, function(data) {
            deferred.resolve( data )
        });
    }, function () {
	// No results when the input contains invalid content
	deferred.resolve( [] );
    } );
    return deferred.promise( { abort: function () {} } );
};
/**
 * @inheritdoc
 */
Trans.ModelLookupTextInputWidget.prototype.getLookupCacheDataFromResponse = function ( response ) {
    return response || [];
};
/**
 * @inheritdoc
 */
Trans.ModelLookupTextInputWidget.prototype.getLookupMenuOptionsFromData = function ( data ) {
    const items = [];
    for ( let i = 0; i < data.length; i++ ) {
	const item = data[ i ];
	items.push( new OO.ui.MenuOptionWidget( {
	    data: item.label,
	    label: item.label
	} ) );
    }
    return items;
};

Trans.ModelLookupTextInputWidget.prototype.onLookupMenuChoose = function ( item ) {
    console.log("ITEM:", item);
    this.setData( item.getData() );
    this.setValue( item.getLabel() );
};
