title;

%let a= D:\\ying_mao\\test.sas;
%let b = D:\\ying_mao\\test2.sas;

%put &a.;
data a;
	first = '<button type="button" onclick="win_run('||"&a."||')">l_aa.sas</button>';
	output;
	first = '<button type="button" onclick="win_run('||"&b."||')">l_bb.sas</button>';
	output;
	first = "&a.";
	output;
run;

data b;
	length first$200;
	first ='<input type = "button" id = "'||"&a."||'" class = "nimi-button" onclick = "win(this);" value = "test.sas" />';
	output;
	first ='<input type = "button" id = "'||"&b."||'" class = "nimi-button" onclick = "win(this);" value = "test2.sas" />';
	output;
run;

/*	function win_run(a) {*/
/*		var cmd = new ActiveXObject("WScript.Shell");*/
/*		cmd.run("cmd.exe /k"+a);*/
/*	}*/


ods html path = "C:\Users\ying_mao\Desktop" file = "aa.html"
	headtext = '
<script type = "text/javascript">

	function win(th){
		var logid = th.id;
		var cmd = new ActiveXObject("WScript.Shell");
		var add = "cmd.exe /k" + logid;
		cmd.run(add);
	}
</script>'
dom;

/*proc print data = a;*/
/*run;*/

proc print data = b;
run;

ods html close;

<button type="button" onclick="win_run(D:\\ying_mao\\test.sas)">l_aa.sas</button>
