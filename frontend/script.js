const apiUrl="https://genai-job-coach-assistant-2.onrender.com/api/generate";
const generateBtn=document.getElementById("generateBtn");
const outputBox=document.getElementById("output")
generateBtn.addEventListener("click",async()=>{
    const role=document.getElementById("role").value.trim();
    const tone=document.getElementById("tone").value;
    const choice=Number(document.getElementById("choice").value)
    const resumeFile=document.getElementById("resume").files[0];
    if(!role){
        alert("Please enter a career role!");
        return;
    }
    outputBox.textContent="Generating... Please wait ";
    generateBtn.disabled=true;
    generateBtn.textContent="Generating...";
    try{
        let response;
        if(resumeFile){
            const formData=new FormData();
            formData.append("role",role);
            formData.append("tone",tone);
            formData.append("choice",choice);
            formData.append("resume",resumeFile);
            response=await fetch(apiUrl,{
                method:"POST",
                body:formData,
            });
        }
        else{
            response=await fetch(apiUrl,{
            method:"POST",
            headers:{
                "Content-Type":"application/json",

            },
            body:JSON.stringify({role,tone,choice})
        });
        }
        if(!response.ok){
            const errText=await response.text();
            outputBox.textContent=`Error :${errText}`
            return
        }
        const data=await response.json();
        let finalOutput="";
        if(data.result){
            finalOutput=JSON.stringify(data.result,null,2);
        }
        else{
            finalOutput=JSON.stringify(data,null,2);
        }
        if (data.resume_preview) {
            const previewSection = document.getElementById("resumePreviewSection");
            const previewBox = document.getElementById("resumePreview");
            previewBox.textContent = data.resume_preview;
            previewSection.style.display = "block";
}

        outputBox.textContent="";
        await typeEffect(finalOutput,outputBox);
    }
    catch(error){
        outputBox.textContent=`Error :${error.message}`;

    }
    finally{
        generateBtn.disabled=false;
        generateBtn.textContent="Generate Response"
    }
});
async function typeEffect(text,element,speed=10) {
    for(let i=0;i<text.length;i++){
        element.textContent+=text.charAt(i);
        await new Promise(resolve=>setTimeout(resolve,speed));
    }
    
}