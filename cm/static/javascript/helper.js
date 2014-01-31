/**
 * Created by preuss on 16.11.13.
 */

/* TODO: Durch http://bootboxjs.com/ ersetzen */
function confirm(msg, url) {
    $('.modal-title').html('Confirm');
    $('.modal-body').html(msg);
    $('#url').prop('href', url);
    $('#modalWindow').modal();
}
