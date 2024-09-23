/*
This file is part of the cintruder project, http://cintruder.03c8.net

Copyright (c) 2012/2016 psy <epsylon@riseup.net>

cintruder is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation version 3 of the License.

cintruder is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along
with cintruder; if not, write to the Free Software Foundation, Inc., 51
Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
*/
window.onload = function() {
    document.getElementById('ifTrack').style.display = 'block';
    document.getElementById('ifTrain').style.display = 'none';
    document.getElementById('ifCrack').style.display = 'none';
    document.getElementById('ifLocal').style.display = 'block';
    document.getElementById('ifUrl').style.display = 'none';
    document.getElementById('ifCrackLocal').style.display = 'block';
    document.getElementById('ifCrackUrl').style.display = 'none';
    document.getElementById('ifMod_set').style.display = 'none';
    document.getElementById('ifMod_set_crack').style.display = 'none';
    document.getElementById('ifMod_colour').style.display = 'none';
    document.getElementById('ifMod_xml').style.display = 'none';
    document.getElementById('Results').style.display = 'none';
    document.getElementById('Captcha-IN').style.display = 'none';
    document.getElementById('OCR-out').style.display = 'none';
}

function SetDefault(){
        document.getElementById('track_url').value = '';
        document.getElementById('track_num').value = '5';
        document.getElementById('tor').checked = false;
        document.getElementById('verbose').checked = false;
        document.getElementById('SourceFile').value = '';
        document.getElementById('train_url').value = '';
        document.getElementById('tor2').checked = false;
        document.getElementById('verbose2').checked = false;
        document.getElementById('set_module').checked = false;
        document.getElementById('use_mod').value = '';
        document.getElementById('set_colour_id').checked = false;
        document.getElementById('set_id').value = '';
        document.getElementById('SourceFile2').value = '';
        document.getElementById('crack_url').value = '';
        document.getElementById('tor3').checked = false;
        document.getElementById('set_module_crack').checked = false;
        document.getElementById('use_mod_crack').value = '';
        document.getElementById('set_xml').checked = false;
        document.getElementById('set_xml_file').value = '';
        document.getElementById('verbose3').checked = false;
        document.getElementById('Results').style.display = 'none';
        document.getElementById('Captcha-IN').style.display = 'none';
        document.getElementById('OCR-out').style.display = 'none';
        document.getElementById('ifMod_set').style.display = 'none';
        document.getElementById('ifMod_set_crack').style.display = 'none';
        document.getElementById('ifMod_colour').style.display = 'none';
        document.getElementById('ifMod_xml').style.display = 'none';
}
function OptionsCheck() {
    if (document.getElementById('track').checked) {
        document.getElementById('ifTrack').style.display = 'block';
        document.getElementById('ifTrain').style.display = 'none';
        document.getElementById('ifCrack').style.display = 'none';
        SetDefault()
    } 
    else if(document.getElementById('train').checked) {
        document.getElementById('ifTrain').style.display = 'block';
        document.getElementById('ifTrack').style.display = 'none';
        document.getElementById('ifCrack').style.display = 'none';
        SetDefault()
        TrainSourcesCheck()
   }
    else if(document.getElementById('crack').checked) {
        document.getElementById('ifCrack').style.display = 'block';
        document.getElementById('ifTrack').style.display = 'none';
        document.getElementById('ifTrain').style.display = 'none';
        SetDefault()
        CrackingCheck()
   }
}
function TrainSourcesCheck() {
   if(document.getElementById('training_local').checked) {
        document.getElementById('ifLocal').style.display = 'block';
        document.getElementById('ifUrl').style.display = 'none';
        SetDefault()
        SetTrainModule()
   }
   else if(document.getElementById('training_url').checked) {
        document.getElementById('ifUrl').style.display = 'block';
        document.getElementById('ifLocal').style.display = 'none';
        SetDefault()
        SetTrainModule()
   }
}
function CrackingCheck() {
   if(document.getElementById('cracking_local').checked) {
        document.getElementById('ifCrackLocal').style.display = 'block';
        document.getElementById('ifCrackUrl').style.display = 'none';
        SetDefault()
        SetCrackModule()
   }
   else if(document.getElementById('cracking_url').checked) {
        document.getElementById('ifCrackUrl').style.display = 'block';
        document.getElementById('ifCrackLocal').style.display = 'none';
        SetDefault()
        SetCrackModule()
   }
}
function SetTrainModule() {
   if((document.getElementById('set_module').checked == true)) {
        document.getElementById('ifMod_set').style.display = 'block';
        document.getElementsByName('train_url')[0].placeholder='Train using a specific OCR exploiting module';
   }
   else{
        document.getElementById("use_mod").value ='';
        document.getElementById('ifMod_set').style.display = 'none';
        document.getElementsByName('train_url')[0].placeholder='Apply common OCR techniques to a remote captcha';
   }
}
function SetColourID() {
   if((document.getElementById('set_colour_id').checked == true)) {
        document.getElementById('ifMod_colour').style.display = 'block';
   }
   else{
        document.getElementById("set_id").value ='';
        document.getElementById('ifMod_colour').style.display = 'none';
   }
}
function SetCrackModule() {
   if((document.getElementById('set_module_crack').checked == true)) {
        document.getElementById('ifMod_set_crack').style.display = 'block';
        document.getElementsByName('crack_url')[0].placeholder='Brute force using a specific OCR exploiting module';
   }
   else if((document.getElementById('set_module_crack').checked == false)) {
        document.getElementById('ifMod_set_crack').style.display = 'none';
        document.getElementsByName('crack_url')[0].placeholder="Brute force using local dictionary (from: 'dictionary/')";
   }
}
function SetXML() {
   if((document.getElementById('set_xml').checked == true)) {
        document.getElementById('ifMod_xml').style.display = 'block';
   }
   else{
        document.getElementById("set_xml_file").value ='';
        document.getElementById('ifMod_xml').style.display = 'none';
   }
}
function loadRemoteOCR(train_url){
       document.getElementById("target_captcha_img_path").src="images/previews/last-preview.gif#"+ new Date().getTime();
       document.getElementById('Captcha-IN').style.display = 'block';
       document.getElementById("directory-words").src = "directory-words";
       document.getElementById("OCR-out").style.display = "block";
}
function loadRemoteOCRCrack(crack_url){
       document.getElementById("target_captcha_img_path").src="images/previews/last-preview.gif#"+ new Date().getTime();
       document.getElementById('Captcha-IN').style.display = 'block';
}
function loadOCRCrack(){
       document.getElementById("target_captcha_img_path").src="images/previews/last-preview.gif#"+ new Date().getTime();
       document.getElementById('Captcha-IN').style.display = 'block';
}
function loadOCR(){
       document.getElementById("target_captcha_img_path").src="images/previews/last-preview.gif#"+ new Date().getTime();
       document.getElementById('Captcha-IN').style.display = 'block';
       document.getElementById("directory-words").src = "directory-words";
       document.getElementById("OCR-out").style.display = "block";
}
function TrackCaptchas(){
        if(document.getElementById("tor").checked) {
        tor="on";
        }else{
        tor="off";
        }
        if(document.getElementById("verbose").checked){
         verbose="on";
        }else{
         verbose="off";
        }
        tracking_source=document.getElementById("track_url").value
        tracking_num=document.getElementById("track_num").value
        if(tracking_source == "") {
          window.alert("You need to enter a valid URL to be tracked!");
          return
         }else{
          params="tracking_source="+escape(tracking_source)+"&tracking_num="+escape(tracking_num)+"&tor="+escape(tor)+"&verbose="+escape(verbose)
         runCommandX("cmd_track",params)
         document.getElementById("Results").style.display = "block";
         }
       }
function TrainCaptchas(){
        document.getElementById('Captcha-IN').style.display = 'none';
        document.getElementById("OCR-out").style.display = "none";
        if(document.getElementById("set_colour_id").checked) 
        {
         colourID=document.getElementById("set_id").value;
        }else {
         colourID="off";
        }
        if(document.getElementById("set_module").checked) 
        {
         module=document.getElementById("use_mod").value;
        }else {
         module="off";
        }
        if(document.getElementById("tor2").checked) 
        {
        tor="on";
        }else {
         tor="off";
        }
        if(document.getElementById("verbose2").checked) 
        {
         verbose="on";
        }else {
         verbose="off";
        }
        source_file=document.getElementById("SourceFile").value;
        train_url=document.getElementById("train_url").value;
        if((source_file == "") && (train_url == "")){
          window.alert("You need to enter any input!");
          return;
         }else{
        if(source_file==""){
        source_file="off"
        }
        params="train_url="+escape(train_url)+"&source_file="+escape(source_file)+"&colourID="+escape(colourID)+"&module="+escape(module)+"&tor="+escape(tor)+"&verbose="+escape(verbose);
         }
         runCommandX("cmd_train",params);
         if(source_file=="off"){
         document.getElementById("Results").style.display = "block";
         setTimeout(function() { loadRemoteOCR(train_url) }, 10000);
         }else{
         document.getElementById("Results").style.display = "block";
         setTimeout("loadOCR()", 6000); // delay 6 on local
         }
}
function CrackCaptchas(){
        document.getElementById('Captcha-IN').style.display = 'none';
        document.getElementById("OCR-out").style.display = "none";
        if(document.getElementById("set_module_crack").checked) 
        {
         module=document.getElementById("use_mod_crack").value;
        }else {
         module="off";
        }
        if(document.getElementById("set_xml").checked)
        {
        xml=document.getElementById("set_xml_file").value;
        }else {
        xml="off";
        }
        if(document.getElementById("tor3").checked) 
        {
        tor="on";
        }else {
         tor="off";
        }
        if(document.getElementById("verbose3").checked) 
        {
         verbose="on";
        }else {
         verbose="off";
        }
        source_file=document.getElementById("SourceFile2").value;
        crack_url=document.getElementById("crack_url").value;
        if((source_file == "") && (crack_url == "")){
          window.alert("You need to enter any input!");
          return;
         }else{
        if(source_file==""){
        source_file="off"
        }
        params="crack_url="+escape(crack_url)+"&source_file="+escape(source_file)+"&module="+escape(module)+"&tor="+escape(tor)+"&verbose="+escape(verbose)+"&xml="+escape(xml);
         }
         runCommandX("cmd_crack",params);
         if(source_file=="off"){
         document.getElementById("Results").style.display = "block";
         setTimeout(function() { loadRemoteOCRCrack(crack_url) }, 10000);
         }else{
         document.getElementById("Results").style.display = "block";
         setTimeout("loadOCRCrack()", 6000); // delay 6 on local
         }
}
function showResults() {
         document.getElementById("Results").style.display = "block";
         document.getElementById('Captcha-IN').style.display = 'none';
         document.getElementById('OCR-out').style.display = 'none';
}
