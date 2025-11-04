from openai import OpenAI
from dotenv import load_dotenv,find_dotenv
import os,json
from template import CAREER_ADVICE_PROMPT,INTERVIEW_QUESTIONS_PROMPT,RESUME_TIPS_PROMPT
dot_env_path=find_dotenv("../.env")
if dot_env_path:
    load_dotenv(dot_env_path)

client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def generate_prompt(template,**kwargs):
    return template.format(**kwargs)
def validate_output(data,required_keys):
    if not isinstance(data,dict):
        print("Validation failed :Output is not a dictionary .")
        return False
    for key in required_keys:
        if key not in data:
            print("Validation Failed :Missing '{key}'")
            return False
    if "skills" in data and not isinstance(data["skills"],list):
        print("Validation failed :'skills' must be list .")
        return False
    if "tip" in data and not isinstance(data["tip"],str):
        print("Validation failed : 'tip' must be a string ")
        return False
    if "questions" in data and not isinstance(data["questions"],list):
        print("Validation failed: 'questions must be list .")
        return False
    if "resume_tips" in data and not isinstance(data["resume_tips"],list):
        print("Validation failed: 'resume_tips' must be a list .")
        return False
    print("Output validation passed\n")
    return True 
def run_prompt(template,resume_text=None,**kwargs):
    if resume_text:
        resume_context=(f"\n\nThe following resume content was provided by the user.\n"
        f"Please use it to make your response more personalized and give suggestions to improve it.\n\n"
        f"{resume_text[:900]}\n\n")
        prompt=generate_prompt(template,**kwargs)+resume_context
    else:
        prompt=generate_prompt(template,**kwargs)
    print("\n Final Prompt sent to the model:\n")
    print(prompt)
    response=client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":"Be concise and Professional"},
            {"role":"user","content":prompt}
        ],
        temperature=0.5,
        max_tokens=150
    )
    raw_output=response.choices[0].message.content.strip()
    print("\n Raw model Output:\n",raw_output)
    try:
        parsed=json.loads(raw_output)
        print("\n Parsed Output:")
        print(json.dumps(parsed,indent=4))
    except json.JSONDecodeError:
        print("JSON Parsing failed .Trying cleanup...")
        cleaned=raw_output[raw_output.find("{"):raw_output.rfind("}")+1]
        try:
            parsed=json.loads(cleaned)
            print("\n Cleaned & Parsed Output: ")
            print(json.dumps(parsed,indent=4))
        except:
            print("\n couldnot parse JSON output correctly.")
            parsed=None
            return parsed
    if parsed:
        if validate_output(parsed,list(parsed.keys())):
            print("\n Final Valid Output Ready for use!\n")
        else:
            parsed=None
            return parsed
    else:
        parsed=None
        return parsed
    return parsed
if __name__=="__main__":
    print("\n Choose a prompt type:\n")
    print("1️⃣Career Advice\n")
    print("2️⃣Interview Question\n")
    print("3️⃣Resume Tips\n")
    choice=input("Enter the choice (1/2/3) :").strip()
    role=input("Enter a career role(e.g Data Analyst,MBA,Cloud Engineer):")
    tone=input("Choose tone (motivational,formal,casual): ")
    if choice=="1":
        res=run_prompt(CAREER_ADVICE_PROMPT,persona="career advisor",role=role,tone=tone,resume_text=None)
    elif choice=="2":
        res=run_prompt(INTERVIEW_QUESTIONS_PROMPT,role=role,tone=tone,resume_text=None)
    elif choice=="3":
        res=run_prompt(RESUME_TIPS_PROMPT,role=role,tone=tone,resume_text=None)
    else:
        print("Invalid choice.")
    if res:
        print("The final Parsed and Validated Output\n",res)
    else:
        print("There was problem in Parsing and Output Validation ,Please try again  ")