dm "log;clear;";
/*options nomprint nomlogic nosymbolgen nofmterr ;*/

options mprint mlogic;

%macro log(path,saspath);

	data loglist;
		rc=filename("mydir","&path.");
		d=dopen("mydir");
		if d gt 0 then do;
			m=dnum(d);
			do i=1 to m;
				name="&path."||dread(d,i);
				if find(name,".log","i")>0 then output;
			end;
		end;
		rc=dclose(d);
		keep name;
	run;

/* **把name连成字符串; &n:how many log files are scanned*/
    proc sql noprint;
	    select name,count(*) into:d separated by "*",:n 
	    from loglist
    ;
    quit;
    %let str = 1;
    %do i = 1 %to &n.;
        %let t = %scan(&d.,&i.,*);
        
        filename logfile "&t.";
        /* 每个log的全部信息 */

        data log&i.;
            infile logfile truncover lrecl = 32767;
            input;
            length content $30000. logname $50;
            logname =scan("&t.",-1,"\");
            content = _infile_;
			n = _n_;
            keep content n;
        run;

/* 。。。特殊情况：处理日志为空的情况 */
        /* data _null_;
            if 0 then set log&i. nobs = lastobs;
            if lastobs == 0 then do;
                call symputx("") */
        
        
        
        data log_&i.;
            length logpath $200.;
            set log&i.;
            logpath="&t.";
            logname =scan(logpath,-1,"\");
			n = _n_;
            if find(content,"WARNING:")>0 
            |find(content,"ERROR:")>0 
            |find(content,"字符值已转换为数值")>0
            |find(content,"数值已转换为字符值")>0
            |find(content,"函数 INPUT 的参数无效")>0
            |find(content,"函数 PUT 的参数无效")>0   
            |find(content,"缺失值的生成是对缺失值执行操作的结果")>0
                    |find(content,"MERGE 语句有多个数据集带有重复的 BY 值")>0
                |find(content,"未初始化")>0   
                    |find(content,"not found or could not be loaded","i")>0
                    |find(content,"uninitialized","i")>0
                    |find(content,"Invalid","i")>0
                    |find(content,"Division by zero","i")>0
                    |find(content,"Missing values were generated","i")>0
                    |find(content,"Numeric values have been converted to character values","i")>0
                    |find(content,"Character values have been converted to numeric values","i")>0
                    |find(content,"MERGE statement has more than one data set with repeats of BY values","i")>0
                    |find(content,"At least one W.D format was too small for the number to be printed","i")>0
                    |find(content,"Character format specified for the result of a numeric expression","i")>0
                    |find(content,"Mathematical operations could not be performed at the following places","i")>0
                    |find(content,"ERROR DETECTED IN ANNOTATE=","i")>0
                    |find(content,"PROBLEM IN OBSERVATION","i")>0
                    |find(content,"Reduction in size of titles","i")>0
                    |find(content,"outside the axis range","i")>0
                    |find(content,"The SAS System stopped processing this step because of insufficient disk space","i")>0
                    |(find(content,"Program run by","i")>0 & index(content,"sysdate9") = 0)
            ;
            if find(content,"Program run by","i")>0 then grp = 1;
            else grp = 2;
            label logname="日志名" content="日志";
        run;
        
        data _null_;
            if 0 then set log_&i. nobs = lastobs;
            call symputx("lastobs",lastobs);
        run;

        data ss&i.;
                set log_&i.;
                where grp  = 2;
				length issueid $200;
                loglink = '<a href="#' || strip(logname) ||'">'||strip(logname)||'</a>';
                issuelink = '<a href = "#'||strip(logname)||strip(put(_n_,best.))||'" >'||strip(content)||'</a>';
/*				logid = '<i id = "'||strip(logname)||'">'||strip(logname)||'</i>';*/
				issueid = '<i id = "'||strip(logname)||strip(put(_n_,best.))||'" >'||strip(content)||'</i>';
/*                keep loglink issuelink;*/
            run;
		
		proc  fcmp outlib=work.funcs.H5;
			function u_label(id$,name$,func$) $; /**/
				
				ret="<i id="||id||" name= '"||name||"' onclick='"||func||"'><font face='Consolas' color=blue>"||id||"</font></i>";	
				return (ret);
			endfunc;
			function code_label(details$) $;
			    length ret $1000;
				ret="<pre><code class='sas'><font face='Consolas' size=1>"||details||"</font></code></pre>";
				return (ret);
		    endfunc;
		
		run; 
/* only logs which have issues */
        %if &lastobs > 1 %then %do;
            %let name =%scan(%scan(&t.,-1,"\"),1,".");
            %let str = &str.*&name.;
           
			data log&i;
				update log&i ss&i;
				by n;
				if ^missing(issueid) then content = strip(issueid);
				drop loglink issuelink;
			run;
            /*the third part on html page，data set name for example：l_aa */
/*            proc sql;*/
/*				select content into: &name. separated by "<\br>" */
/*				from log&i.;*/
/*			quit;*/
/*			%put %nrbquote(&&&name.);*/

/*			%put _all_;*/
/*			%put &L_EQ5D;*/
/*			%let aa = %nrstr(&nam*/
/*			%put _all_;*/
/*			%put %str(&&&name.);*/
/*			data &name.;*/
/*				call streaminit(10000);*/
/*				length logpath$200. logname$50.;*/
/*				logpath = "&t.";*/
/*				sasname = "&name."||".sas";*/
/*				content = %nrbquote(&&&name.);*/
/*			run;*/
	/*html third part		*/
			data &name.(keep = logi);
				length logi $30000.;
				retain logi;
				set log&i. end = last;
				logi = strip(logi)||"<br />"||content;
				if length(logi) > 27000 then do;
					output;
					stop;
				end;
 				else if last then output;				
			run;
			
			data &name.;
				length log $30000.;
				set &name.;
				log = "<pre><code class='sas'><font face='Consolas' size=1>"||strip(logi)||"</font></code></pre>";
				drop logi;
			run;
			
			data &name.1;
				set &name.;
				length forcmd $300.;				
				forcmd = '<i id ="'||"&name."||'.log'||'" name = "'||"&saspath."||"&name."||'.sas'||'" onclick = "cs(this);" >'||"&name."||'.sas</i>';
			run;
        %end;
                    
        %if &i.=1 %then %do;
            data logissues;
                set log_&i.;
            run;
        	
			data alog;
				set ss&i.;
			run; 
	    %end;
	    %else %do;
            data logissues;
                set logissues log_&i.;
            run;

			data alog;
				set alog ss&i.;
			run;
	    %end;        
    %end;

    
    /* 有时间记录的logname数*/
    /* 。。。这里想到特殊情况：没有时间记录的logfile */
    proc sql;
        select count(distinct logname ) into:scanned
        from logissues;
    quit;

     
    data dateissue;
        set logissues;
        where grp = 1;
        length authour$20. str$1000.;
            authour = scan(content,5);
            updatedt = scan(content,7);
            nowdate = "&sysdate9.";
            cha = input(nowdate,date9.) - input(updatedt,date9.);
            str = "file:"||strip(logname)||'0d0a'x||"authour:"||strip(authour)||'0d0a'x||"lastest updated date:"||updatedt;
        if cha gt 7;
    run;

/*suspected not executed for a long time */
    proc sql;
        select str into: dateiss separated by '0d0a'x
        from dateissue;
    quit;

/* log issues and log clear */
    proc sql;
        select count(*),&n.-count(distinct loglink),count(distinct loglink) into:issues,:logclear,:logfor from alog;
    quit;

    /* summary table */
    data summary;
        length item $100. value$1000.;
        item = "how many log files are scanned";
        value = strip("&n");
        output;
        item = "suspected not executed for a long time";
        value = strip("&dateiss");
        output;
        item = "log clear";
        value = strip("&logclear");
        output;
        item = "log issue(s)";
        value = strip("&issues");
        output;
        item = "file path";
        value = strip("&path");
        output;
    run;
	
	%let environment=<link href='./idea.css' rel='stylesheet'><script src='./hlsas.js'></script>;

	ods html path="C:\users\a\desktop" file="index.html" 
	headtext="&environment.<script>hljs.initHighlightingOnLoad();function cs(e){var N=e.name;var o=new ActiveXObject('WScript.Shell');var c='cmd.exe /c'+N;o.Run(c)}</script>";
	
	title '<i id = "top">log summary</i>';
	proc report data = summary nowindows missing split = '#'
        style(column) = {just=l asis=on protectspecialchars = off};
		column item value;
		define item/display;
		define value /display;
	run;
	
	title "log issues";
	proc print data = alog noobs;
		var loglink issuelink;
	run;

	proc reprot data = alog nowindows missing split = '#'
        style(column) = {just=l asis=on protectspecialchars = off};
		column loglink issuelink;
		display loglink/group;
		display issuelink/group;
	run;
	
	%do i = 2 %to &logfor + 1;
		 %let name = %scan(&str,&i,*);
		 title '<a href = "#top">'&name.(back to top)'</a>';
		 proc print data = &name.1 noobs;
		 run;
	%end;
	ods html close;
	title;

%mend;

%log(path = %nrstr(C:\Users\a\Desktop\项目\), saspath = %nrstr(C:\Users\a\Desktop\项目\));












