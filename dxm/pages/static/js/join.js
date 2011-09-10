var ADDURL = $ADDURL
var signingUp = false;

function signUpClicked()
{
	if(signingUp) return;
	signingUp = true;
	var name = $("#joinname").val();
	if(name.length <= 0)
	{
		alert("Please enter your name");
		signingUp = false;
		return;
	}
	var email = $("#joinemail").val();
	if(email.length <= 0)
	{
		alert("Please enter your email");
		signingUp = false;
		return;
	}
	if(email.search(/\S+@\S+/) != 0)
	{
		alert("Please enter a valid email address");
		signingUp = false;
		return;
	}
	var note = $("#joinnote").val();
	addPotentialMember(name, email, note, memberAdded);
}

function memberAdded()
{
	$('#joinform').hide();
	$('#success-message').show();
	signingUp = false;
}

function addPotentialMember(name, email, note, callbackFn)
{
	$.post(
		ADDURL,
		{"name": name, "email": email, "note": note, "csrfmiddlewaretoken": $CSRFTOKEN},
		callbackFn
	)
}