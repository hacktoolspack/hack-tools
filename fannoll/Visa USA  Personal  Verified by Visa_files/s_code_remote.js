/************************ ADDITIONAL FEATURES ************************
     Dynamic Account Selection
     Plugins
*/
/************************** CONFIG SECTION **************************/
/* You may add or alter any code config here.                       */
/* Specify the Report Suite ID(s) to track here */

// Dynamic Accounts configured: if domain is usa.visa.com/personal/security/vbv then traffic
// will go to visausavbvcom. If the domain is usa.visa.com/visaextras then traffic will go to
// visausaextrascom automatically.
var s_account="visausaextrascom"
var s_dynamicAccountSelection=true
var s_dynamicAccountList="visausaextrascom=usa.visa.com/visaextras;visausavbvcom=usa.visa.com/personal/security/vbv,usa.visa.com/personal/security/visa_security_program/vbv"
var s_dynamicAccountMatch=window.location.host+window.location.pathname;

/* Link Tracking Config */
var s_trackDownloadLinks=true
var s_trackExternalLinks=true
var s_trackInlineStats=true
var s_linkDownloadFileTypes="exe,zip,wav,mp3,mov,mpg,avi,wmv,doc,pdf,xls"
var s_linkInternalFilters="javascript:,usa.visa.com"
var s_linkLeaveQueryString=false
var s_linkTrackVars="s_eVar1,s_eVar2,s_events"
var s_linkTrackEvents="event1"
/* Plugin Config */
var s_usePlugins=true
function s_doPlugins() {
	/* Add calls to plugins here */
}

/************************** PLUGINS SECTION *************************/
/* You may insert any plugins you wish to use here.                 */
/*
 * Plugin: Get Query String CGI Variable Value
 */
function s_vp_getCGI(vs,k)
	{var v='';if(k&&s_wd.location.search){var q=s_wd.location.search,
	qq=q.indexOf('?');q=qq<0?q:q.substring(qq+1);v=s_pt(q,'&',s_cgif,
	k)}s_vpr(vs,v)}function s_cgif(t,k){if(t){var te=t.indexOf('='),
	sk=te<0?t:t.substring(0,te),sv=te<0?'True':t.substring(te+1);if(
	sk==k)return s_epa(sv)}return ''}
/*
 * Plugin Utilities v2.0 (Required For All Plugins)
 */
function s_vpr(vs,v){if(s_wd[vs])s_wd[vs]=s_wd[vs];else s_wd[vs]=''
if(vs.substring(0,2) == 's_')vs=vs.substring(2);s_wd['s_vpv_'+vs]=v
s_wd['s_vpm_'+vs]=1}function s_dt(tz,t){var d=new Date;if(t)d.setTime(
t);d=new Date(d.getTime()+(d.getTimezoneOffset()*60*1000))
return new Date(Math.floor(d.getTime()+(tz*60*60*1000)))}
function s_vh_gt(k,v){var vh='|'+s_c_r('s_vh_'+k),vi=vh.indexOf('|'+v
+'='),ti=vi<0?vi:vi+2+v.length,pi=vh.indexOf('|',ti),t=ti<0?'':
vh.substring(ti,pi<0?vh.length:pi);return t}function s_vh_gl(k){var
vh=s_c_r('s_vh_'+k),e=vh?vh.indexOf('='):0;return vh?(vh.substring(0,
e?e:vh.length)):''}function s_vh_s(k,v){if(k&&v){var e=new Date,st=
e.getTime(),y=e.getYear(),c='s_vh_'+k,vh='|'+s_c_r(c)+'|',t=s_vh_gt(k,
v);e.setYear((y<1900?y+1900:y)+5);if(t)vh=s_rep(vh,'|'+v+'='+t+'|','|'
);if(vh.substring(0,1)=='|')vh=vh.substring(1);if(vh.substring(
vh.length-1,vh.length)=='|')vh=vh.substring(0,vh.length-1);vh=v
+'=[PCC]'+(vh?'|'+vh:'');s_c_w(c,vh,e);if(s_vh_gt(k,v)!='[PCC]')
return 0;vh=s_rep(vh,'[PCC]',st);s_c_w(c,vh,e)}return 1}

/************* DO NOT ALTER ANYTHING BELOW THIS LINE ! **************/
var s_un,s_ios=0,s_q='',s_code='',code='',s_bcr=0,s_lnk='',s_eo='',
s_vb,s_pl,s_tfs=0,s_etfs=0,s_wd=window,s_d=s_wd.document,s_ssl=(
s_wd.location.protocol.toLowerCase().indexOf('https')>=0),s_n=
navigator,s_u=s_n.userAgent,s_apn=s_n.appName,s_v=s_n.appVersion,
s_apv,s_i,s_ie=s_v.indexOf('MSIE '),s_ns6=s_u.indexOf('Netscape6/')
if(s_v.indexOf('Opera')>=0||s_u.indexOf('Opera')>=0)s_apn='Opera';var
s_isie=(s_apn=='Microsoft Internet Explorer'),s_isns=(s_apn==
'Netscape'),s_isopera=(s_apn=='Opera'),s_ismac=(s_u.indexOf('Mac')>=0)
if(s_ie>0){s_apv=parseInt(s_i=s_v.substring(s_ie+5));if(s_apv>3)s_apv=
parseFloat(s_i)}else if(s_ns6>0)s_apv=parseFloat(s_u.substring(s_ns6
+10));else s_apv=parseFloat(s_v);function s_fl(s,l){return (s+''
).substring(0,l)}function s_co(o){if(!o)return o;var n=new Object,x
for(x in o)if(x.indexOf("select")<0&&x.indexOf("filter")<0)n[x]=o[x]
return n}function s_num(x){var s=x.toString(),g='0123456789',p,d
for(p=0;p<s.length;p++){d=s.substring(p,p+1);if(g.indexOf(d)<0)
return 0}return 1}function s_rep(s,o,n){var i=s.indexOf(o),l=n.length>
0?n.length:1;while(s&&i>=0){s=s.substring(0,i)+n+s.substring(i
+o.length);i=s.indexOf(o,i+l)}return s}function s_ape(s){return s?
s_rep(escape(''+s),'+','%2B'):s}function s_epa(s){return s?unescape(
s_rep(''+s,'+',' ')):s}function s_pt(s,d,f,a){var t=s,x=0,y,r;while(t)
{y=t.indexOf(d);y=y<0?t.length:y;t=t.substring(0,y);r=f(t,a);if(r)
return r;x+=y+d.length;t=s.substring(x,s.length);t=x<s.length?t:''}
return ''}function s_isf(t,a){if(t.substring(0,2)=='s_')t=t.substring(
2);return (t!=''&&t==a)}function s_fsf(t,a){if(s_pt(a,',',s_isf,t))
s_fsg+=(s_fsg!=''?',':'')+t;return 0}var s_fsg;function s_fs(s,f){
s_fsg='';s_pt(s,',',s_fsf,f);return s_fsg}var s_c_d=''
function s_c_gdf(t,a){if(!s_num(t))return 1;return 0}function s_c_gd()
{var d=s_wd.location.hostname,n=s_gg('cookieDomainPeriods'),p;if(d&&
!s_c_d){n=n?parseInt(n):2;n=n>2?n:2;p=d.lastIndexOf('.');while(p>=0&&
n>1){p=d.lastIndexOf('.',p-1);n--}s_c_d=p>0&&s_pt(d,'.',s_c_gdf,0)?
d.substring(p):''}return s_c_d}function s_c_r(k){k=s_ape(k);var c=' '
+s_d.cookie,s=c.indexOf(' '+k+'='),e=s<0?s:c.indexOf(';',s),v=s<0?'':
s_epa(c.substring(s+2+k.length,e<0?c.length:e));return v!='[[B]]'?v:''
}function s_c_w(k,v,e){var d=s_c_gd(),l=s_gg('cookieLifetime'),s;v=''
+v;l=l?(''+l).toUpperCase():'';if(e&&l!='SESSION'&&l!='NONE'){s=(v!=
''?parseInt(l?l:0):-60);if(s){e=new Date;e.setTime(e.getTime()+(s*1000
))}}if(k&&l!='NONE'){s_d.cookie=k+'='+s_ape(v!=''?v:'[[B]]')+'; '
+'path=/;'+(e&&l!='SESSION'?' expires='+e.toGMTString()+';':'')+(d?
' domain='+d+';':'');return s_c_r(k)==v}return 0}function s_cet(f,a,
et,oe,fb){var r,d=0
/*@cc_on@if(@_jscript_version>=5){try{return f(a)}catch(e){return et(e)}d=1}@end@*/
if(!d){if(s_ismac&&s_u.indexOf('MSIE 4')>=0)return fb(a);else{
s_wd.s_oe=s_wd.onerror;s_wd.onerror=oe;r=f(a);s_wd.onerror=s_wd.s_oe
return r}}}function s_gtfset(e){return s_tfs}function s_gtfsoe(e){
s_wd.onerror=s_wd.s_oe;s_etfs=1;var code=s_gs(s_un);if(code)s_d.write(
code);s_etfs=0;return true}function s_gtfsfb(a){return s_wd}
function s_gtfsf(w){var p=w.parent,l=w.location;s_tfs=w;if(p&&
p.location!=l&&p.location.host==l.host){s_tfs=p;return s_gtfsf(s_tfs)}
return s_tfs}function s_gtfs(){if(!s_tfs){s_tfs=s_wd;if(!s_etfs)s_tfs=
s_cet(s_gtfsf,s_tfs,s_gtfset,s_gtfsoe,s_gtfsfb)}return s_tfs}
function s_ca(un){un=un.toLowerCase();var ci=un.indexOf(','),fun=ci<0?
un:un.substring(0,ci),imn='s_i_'+fun;if(s_d.images&&s_apv>=3&&
!s_isopera&&(s_ns6<0||s_apv>=6.1)){s_ios=1;if(!s_d.images[imn]&&(
!s_isns||(s_apv<4||s_apv>=5))){s_d.write('<im'+'g name="'+imn
+'" height=1 width=1 border=0 alt="">');if(!s_d.images[imn])s_ios=0}}}
function s_it(un){s_ca(un)}function s_mr(un,sess,q,ta){un=
un.toLowerCase();var ci=un.indexOf(','),fun=ci<0?un:un.substring(0,ci
),unc=s_rep(fun,'_','-'),imn='s_i_'+fun,im,b,e,rs='http'+(s_ssl?'s':''
)+'://'+(s_ssl?'102':unc)+'.112.2O7.net/b/ss/'+un+'/1/G.7-PD-R/'
+sess+'?[AQB]&ndh=1'+(q?q:'')+(s_q?s_q:'')+'&[AQE]';if(s_ios){im=s_wd[
imn]?s_wd[imn]:s_d.images[imn];if(!im)im=s_wd[imn]=new Image;im.src=rs
if(rs.indexOf('&pe=')>=0&&(!ta||ta=='_self'||ta=='_top'||(s_wd.name&&
ta==s_wd.name))){b=e=new Date;while(e.getTime()-b.getTime()<500)e=
new Date}return ''}return '<im'+'g sr'+'c="'+rs
+'" width=1 height=1 border=0 alt="">'}function s_gg(v){var g='s_'+v
return s_wd[g]||s_wd.s_disableLegacyVars?s_wd[g]:s_wd[v]}var s_qav=''
function s_havf(t,a){var b=t.substring(0,4),s=t.substring(4),n=
parseInt(s),k='s_g_'+t,m='s_vpm_'+t,q=t,v=s_gg('linkTrackVars'),e=
s_gg('linkTrackEvents');if(!s_wd['s_'+t])s_wd['s_'+t]='';s_wd[k]=s_wd[
m]?s_wd['s_vpv_'+t]:s_gg(t);if(s_lnk||s_eo){v=v?v+',pageName,pageURL,'
+'referrer,charSet,cookieDomainPeriods,cookieLifetime,currencyCode,pu'
+'rchaseID':'';if(v&&!s_pt(v,',',s_isf,t))s_wd[k]='';if(t=='events'&&e
)s_wd[k]=s_fs(s_wd[k],e)}s_wd[m]=0;if(t=='pageURL')q='g';else if(t==
'referrer')q='r';else if(t=='charSet')q='ce';else if(t==
'cookieDomainPeriods')q='cdp';else if(t=='cookieLifetime')q='cl'
else if(t=='currencyCode')q='cc';else if(t=='channel')q='ch';else if(
t=='campaign')q='v0';else if(s_num(s)){if(b=='prop')q='c'+n;else if(
b=='eVar')q='v'+n;else if(b=='hier')q='h'+n}if(s_wd[k]&&t!=
'linkName'&&t!='linkType')s_qav+='&'+q+'='+s_ape(s_wd[k]);return ''}
function s_hav(){var n,av='charSet,cookieDomainPeriods,cookieLifetime'
+',pageName,pageURL,referrer,channel,server,pageType,campaign,state,z'
+'ip,events,products,currencyCode,purchaseID,linkName,linkType'
for(n=1;n<26;n++)av+=',prop'+n+',eVar'+n+',hier'+n;s_qav='';s_pt(av,
',',s_havf,0);return s_qav}function s_lnf(t,h){t=t?t.toLowerCase():''
h=h?h.toLowerCase():'';var te=t.indexOf('=');if(t&&te>0&&h.indexOf(
t.substring(te+1))>=0)return t.substring(0,te);return ''}
function s_ln(h){if(s_gg('linkNames'))return s_pt(s_gg('linkNames'),
',',s_lnf,h);return ''}function s_ltdf(t,h){t=t?t.toLowerCase():'';h=
h?h.toLowerCase():'';var qi=h.indexOf('?');h=qi>=0?h.substring(0,qi):h
if(t&&h.substring(h.length-(t.length+1))=='.'+t)return 1;return 0}
function s_ltef(t,h){t=t?t.toLowerCase():'';h=h?h.toLowerCase():'';if(
t&&h.indexOf(t)>=0)return 1;return 0}function s_lt(h){var lft=s_gg(
'linkDownloadFileTypes'),lef=s_gg('linkExternalFilters'),lif=s_gg(
'linkInternalFilters')?s_gg('linkInternalFilters'):
s_wd.location.hostname;h=h.toLowerCase();if(s_gg('trackDownloadLinks'
)&&lft&&s_pt(lft,',',s_ltdf,h))return 'd';if(s_gg('trackExternalLinks'
)&&(lef||lif)&&(!lef||s_pt(lef,',',s_ltef,h))&&(!lif||!s_pt(lif,',',
s_ltef,h)))return 'e';return ''}function s_lc(e){s_lnk=s_co(this)
s_gs('');s_lnk='';if(this.s_oc)return this.s_oc(e);return true}
function s_ls(){var l,ln,oc;for(ln=0;ln<s_d.links.length;ln++){l=
s_d.links[ln];oc=l.onclick?l.onclick.toString():'';if(oc.indexOf(
"s_gs(")<0&&oc.indexOf("s_lc(")<0){l.s_oc=l.onclick;l.onclick=s_lc}}}
function s_bc(e){s_eo=e.srcElement?e.srcElement:e.target;s_gs('')
s_eo=''}function s_ot(o){var a=o.type,b=o.tagName;return (a&&
a.toUpperCase?a:b&&b.toUpperCase?b:o.href?'A':'').toUpperCase()}
function s_oid(o){var t=s_ot(o),p=o.protocol,c=o.onclick,n='',x=0;if(
!o.s_oid){if(o.href&&(t=='A'||t=='AREA')&&(!c||!p||p.toLowerCase(
).indexOf('javascript')<0))n=o.href;else if(c){n=s_rep(s_rep(s_rep(
s_rep(c.toString(),"\r",''),"\n",''),"\t",''),' ','');x=2}else if(
o.value&&(t=='INPUT'||t=='SUBMIT')){n=o.value;x=3}else if(o.src&&t==
'IMAGE')n=o.src;if(n){o.s_oid=s_fl(n,100);o.s_oidt=x}}return o.s_oid}
function s_rqf(t,un){var e=t.indexOf('='),u=e>=0?','+t.substring(0,e)
+',':'';return u&&u.indexOf(','+un+',')>=0?s_epa(t.substring(e+1)):''}
function s_rq(un){var c=un.indexOf(','),v=s_c_r('s_sq'),q='';if(c<0)
return s_pt(v,'&',s_rqf,un);return s_pt(un,',',s_rq,0)}var s_sqq,s_squ
function s_sqp(t,a){var e=t.indexOf('='),q=e<0?'':s_epa(t.substring(e
+1));s_sqq[q]='';if(e>=0)s_pt(t.substring(0,e),',',s_sqs,q);return 0}
function s_sqs(un,q){s_squ[un]=q;return 0}function s_sq(un,q){s_sqq=
new Object;s_squ=new Object;s_sqq[q]='';var k='s_sq',v=s_c_r(k),x,c=0
s_pt(v,'&',s_sqp,0);s_pt(un,',',s_sqs,q);v='';for(x in s_squ)s_sqq[
s_squ[x]]+=(s_sqq[s_squ[x]]?',':'')+x;for(x in s_sqq)if(x&&s_sqq[x]&&(
x==q||c<2)){v+=(v?'&':'')+s_sqq[x]+'='+s_ape(x);c++}return s_c_w(k,v,0
)}function s_wdl(e){s_wd.s_wd_l=1;var r=true;if(s_wd.s_ol)r=s_wd.s_ol(
e);if(s_wd.s_ls)s_wd.s_ls();return r}function s_wds(un){un=
un.toLowerCase();s_wd.s_wd_l=1;if(s_apv>3&&(!s_isie||!s_ismac||s_apv>=
5)){s_wd.s_wd_l=0;if(!s_wd.s_unl)s_wd.s_unl=new Array;s_wd.s_unl[
s_wd.s_unl.length]=un;if(s_d.body&&s_d.body.attachEvent){if(
!s_wd.s_bcr&&s_d.body.attachEvent('onclick',s_bc))s_wd.s_bcr=1}
else if(s_d.body&&s_d.body.addEventListener){if(!s_wd.s_bcr&&
s_d.body.addEventListener('click',s_bc,false))s_wd.s_bcr=1}else{var
ol=s_wd.onload?s_wd.onload.toString():'';if(ol.indexOf("s_wdl(")<0){
s_wd.s_ol=s_wd.onload;s_wd.onload=s_wdl}}}}function s_iepf(i,a){if(
i.substring(0,1)!='{')i='{'+i+'}';if(s_d.body.isComponentInstalled(i,
'ComponentID')){var n=s_pl.length;s_pl[n]=new Object;s_pl[n].name=i
+':'+s_d.body.getComponentVersion(i,'ComponentID')}return 0}
function s_vs(un,x){var s=s_gg('visitorSampling'),g=s_gg(
'visitorSamplingGroup'),k='s_vsn_'+un+(g?'_'+g:''),n=s_c_r(k),e=
new Date,y=e.getYear();e.setYear(y+10+(y<1900?1900:0));if(s){s*=100
if(!n){if(!s_c_w(k,x,e))return 0;n=x}if(n%10000>s)return 0}return 1}
function s_dyasmf(t,m){if(t&&m&&m.indexOf(t)>=0)return 1;return 0}
function s_dyasf(t,m){var i=t?t.indexOf('='):-1,un,s;if(i>=0&&m){var
un=t.substring(0,i),s=t.substring(i+1);if(s_pt(s,',',s_dyasmf,m))
return un}return 0}function s_dyas(un,l,m){if(!m)m=s_wd.location.host
if(!m.toLowerCase)m=m.toString();l=l.toLowerCase();m=m.toLowerCase()
var nun=s_pt(l,';',s_dyasf,m);if(nun)return nun;return un}
function s_gs(un){un=un.toLowerCase()
var dyas=s_gg('dynamicAccountSelection'),dyal=s_gg(
'dynamicAccountList'),dyam=s_gg('dynamicAccountMatch');if(dyas&&dyal)
un=s_dyas(un,dyal,dyam);
s_un=un;var trk=1,tm=new Date,sed=Math&&Math.random?Math.floor(
Math.random()*10000000000000):tm.getTime(),sess='s'+Math.floor(
tm.getTime()/10800000)%10+sed,yr=tm.getYear(),tfs=s_gtfs(),t,ta='',q=
'',qs='';yr=yr<1900?yr+1900:yr;t=tm.getDate()+'/'+tm.getMonth()+'/'+yr
+' '+tm.getHours()+':'+tm.getMinutes()+':'+tm.getSeconds()+' '
+tm.getDay()+' '+tm.getTimezoneOffset();if(!s_q){var tl=tfs.location,
s='',c='',v='',p='',bw='',bh='',j='1.0',k=s_c_w('s_cc','true',0)?'Y':
'N',hp='',ct='',iepl=s_gg('iePlugins'),pn=0,ps;if(s_apv>=4)s=
screen.width+'x'+screen.height;if(s_isns||s_isopera){if(s_apv>=3){j=
'1.1';v=s_n.javaEnabled()?'Y':'N';if(s_apv>=4){j='1.2';c=
screen.pixelDepth;bw=s_wd.innerWidth;bh=s_wd.innerHeight;if(s_apv>=
4.06)j='1.3'}}s_pl=s_n.plugins}else if(s_isie){if(s_apv>=4){v=
s_n.javaEnabled()?'Y':'N';j='1.2';c=screen.colorDepth;if(s_apv>=5){bw=
s_d.documentElement.offsetWidth;bh=s_d.documentElement.offsetHeight;j=
'1.3';if(!s_ismac&&s_d.body){s_d.body.addBehavior("#default#homePage")
hp=s_d.body.isHomePage(tl)?"Y":"N";s_d.body.addBehavior(
"#default#clientCaps");ct=s_d.body.connectionType;if(iepl){s_pl=
new Array;s_pt(iepl,',',s_iepf,'');}}}}else r='';if(!s_pl&&iepl)s_pl=
s_n.plugins}if(s_pl)while(pn<s_pl.length&&pn<30){ps=s_fl(s_pl[pn
].name,100)+';';if(p.indexOf(ps)<0)p+=ps;pn++}s_q=(s?'&s='+s_ape(s):''
)+(c?'&c='+s_ape(c):'')+(j?'&j='+j:'')+(v?'&v='+v:'')+(k?'&k='+k:'')+(
bw?'&bw='+bw:'')+(bh?'&bh='+bh:'')+(ct?'&ct='+s_ape(ct):'')+(hp?'&hp='
+hp:'')+(s_vb?'&vb='+s_vb:'')+(p?'&p='+s_ape(p):'')}if(s_gg(
'usePlugins'))s_wd.s_doPlugins();var l=s_wd.location,r=
tfs.document.referrer;if(!s_gg("pageURL"))s_wd.s_pageURL=s_fl(l?l:'',
255);if(!s_gg("referrer"))s_wd.s_referrer=s_fl(r?r:'',255);q+=(t?'&t='
+s_ape(t):'')+s_hav();if(s_lnk||s_eo){var o=s_eo?s_eo:s_lnk;if(!o)
return '';var p=s_wd.s_g_pageName,w=1,t=s_ot(o),n=s_oid(o),x=o.s_oidt,
h,l,i,oc;if(s_eo&&o==s_eo){while(o&&!n&&t!='BODY'){o=o.parentElement?
o.parentElement:o.parentNode;if(!o)return '';t=s_ot(o);n=s_oid(o);x=
o.s_oidt}oc=o.onclick?o.onclick.toString():'';if(oc.indexOf("s_gs(")>=
0)return ''}ta=o.target;h=o.href?o.href:'';i=h.indexOf('?');h=s_gg(
'linkLeaveQueryString')||i<0?h:h.substring(0,i);l=s_gg('linkName')?
s_gg('linkName'):s_ln(h);t=s_gg('linkType')?s_gg('linkType'
).toLowerCase():s_lt(h);if(t&&(h||l))q+='&pe=lnk_'+(t=='d'||t=='e'?
s_ape(t):'o')+(h?'&pev1='+s_ape(h):'')+(l?'&pev2='+s_ape(l):'');else
trk=0;if(s_gg('trackInlineStats')){if(!p){p=s_wd.s_g_pageURL;w=0}t=
s_ot(o);i=o.sourceIndex;if(s_gg('objectID')){n=s_gg('objectID');x=1;i=
1}if(p&&n&&t)qs='&pid='+s_ape(s_fl(p,255))+(w?'&pidt='+w:'')+'&oid='
+s_ape(s_fl(n,100))+(x?'&oidt='+x:'')+'&ot='+s_ape(t)+(i?'&oi='+i:'')}
s_wd.s_linkName=s_wd.s_linkType=s_wd.s_objectID=s_lnk=s_eo='';if(
!s_wd.s_disableLegacyVars)s_wd.linkName=s_wd.linkType=s_wd.objectID=''
}if(!trk&&!qs)return '';var code='';if(un){if(trk&&s_vs(un,sed))code+=
s_mr(un,sess,q+(qs?qs:s_rq(un)),ta);s_sq(un,trk?'':qs)}else if(
s_wd.s_unl)for(var unn=0;unn<s_wd.s_unl.length;unn++){un=s_wd.s_unl[
unn];if(trk&&s_vs(un,sed))code+=s_mr(un,sess,q+(qs?qs:s_rq(un)),ta)
s_sq(un,trk?'':qs)}return code}function s_dc(un){un=un.toLowerCase()
var dyas=s_gg('dynamicAccountSelection'),dyal=s_gg(
'dynamicAccountList'),dyam=s_gg('dynamicAccountMatch');if(dyas&&dyal)
un=s_dyas(un,dyal,dyam);
s_wds(un);s_ca(un);return s_gs(un)}
s_code=s_dc(s_account);if(s_code)s_d.write(s_code)
