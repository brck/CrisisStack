$(document).ready(function() {
	$(".developer").hide();
});

$(document).on('change','#account_type',function(){
	var account_type = $('#account_type').val();

	if (account_type === 'Developer') {
		$(".developer").show();
	} else {
		$(".developer").hide();
	}
});
