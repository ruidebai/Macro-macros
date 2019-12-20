/*---------author:wenqi_qin---------*/

/*Log summary simulation data*/
data summary;
	length item value $200.;
	item="how many log files are scaned";
	value=strip(put(18,best.));
	output;
	item="suspected not executed for a long time";
	value="file:l_bb.log"||"^n"||"latest updated date:20April2019";
	output;
	item="log clear";
	value=strip(put(16,best.));
	output;
	item="log issue(s)";
	value=strip(put(2,best.));
	output;
	item="file path";
	value="C:/Users/a/desktop/project/log/";
	output;
run;




/*make a  dummy data to simulate error details*/

data details;
	call streaminit(10000);
	length name $200. error warning notes 8.;
	do i =1 to 10;
	name="demo_"||strip(put(i,best.))||".log";
	error=abs(int(rand("normal")*10));
	warning=abs(int(rand("normal")*10));
	notes=abs(int(rand("normal")*10));
	output;
	end;
	drop i;
run;

proc sort;
	by name;
run;



/*log information for each log*/
data info;
	call streaminit(10000);
	length name alias  Info $200.;
	do i =1 to 10;
	name="demo_"||strip(put(i,best.))||".log";
	alias='<a id="' || trim(name) ||'">'||trim(name)||'</a> ';
	Info="<code=sas'>NOTE: There were"||strip(abs(int(rand("normal")*10)))||" observations read from the data set WORK.FINAL.</code>";
	output;
	end;
	drop  name;
run;

data _null_;
	if 0 then set info nobs=n;
		call symput("obs",n);
run;


proc sort;
	by alias;
run;
ods _all_ close;
   
proc template;
    define table gallery;
        column name error warning notes links;
        define links;
           header = 'Links';
           compute as '<a href="#' || trim(name) ||'">²é¿´</a> ';
        end;
end;
run;


ods html path="C:\Users\a\Desktop" file="index.html";
title "Log Summary"; 
proc report data=summary nowindows missing;
	column item value;
	define item/display;
	define value/display;
run;
title "Details of each log file";
data _null_;
        set details(where=(error ^=0));
        file print ods=(template='Gallery');
        put _ods_;
run;
title;   
%macro printHtml(datas);
	%do i=1 %to &obs.;
	data s;
		set &datas.;
		where i=&obs.;
    run;
	proc report data = s nowindows missing split='#';
	  column alias info;
	  define alias/display;
	  define info/display;
	run;
	%end;
%mend printHtml;
%printHtml(info)
ods html close;
