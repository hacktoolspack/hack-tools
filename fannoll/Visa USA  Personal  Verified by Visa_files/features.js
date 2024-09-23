  function contains(arrayObj, obj){
    var i;
    for(i=0; i<arrayObj.length; i++){
      if(arrayObj[i]==obj) break;
    }
    return i<arrayObj.length;
  } 
  
  var alreadyShown=new Array();
  
  function showRandomFeature(){
    var i,j,k,l,m;
  
		if((typeof randomize) == "undefined" || randomize=="yes"){
  		var tw=0;
      for(m=0; m<weights.length; m++){
        if(!contains(alreadyShown,m)) tw+=weights[m];
      }
      
      k=Math.round(Math.random()*(tw));
  
      for(j=0; j<weights.length; j++){
        if(contains(alreadyShown,j)) continue;
        k-=weights[j];
        if(k<=0) break;
      }
		}else{
		  var maxwt=0;
      for(m=0; m<weights.length; m++){
        if(!contains(alreadyShown,m) && maxwt<weights[m]) maxwt=weights[m];
      }
      for(j=0; j<weights.length; j++){
        if(contains(alreadyShown,j)) continue;
        if(weights[j]==maxwt) break;
      }
		}
    
    alreadyShown[alreadyShown.length]=j;
    if(j<features.length){
		  if(features[j].match( /^\s*$/ ) == null){
        i=features[j].replace(/\%POS\%/g, new String(alreadyShown.length)).
          replace(/\%RND\%/g,new String(Math.random()*1000000000));
        //alert(i);
        document.write(i);
			}else{
			  showRandomFeature();
			}
    }
  }
