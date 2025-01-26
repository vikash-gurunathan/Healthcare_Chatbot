from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from fuzzywuzzy import process

app = Flask(__name__)
CORS(app)

# Healthcare knowledge base categorized by question types
healthcare_knowledge_base = {
    "what": {
    "what is healthcare": "Healthcare is the organized provision of medical care to individuals or a community.",
    "what is hypertension": "Hypertension, also known as high blood pressure, is a condition where the force of the blood against the artery walls is too high.",
    "what is diabetes": "Diabetes is a disease that occurs when your blood sugar, or glucose, is too high.",
    "what is cancer": "Cancer is a group of diseases characterized by the uncontrolled growth of abnormal cells.",
    "what is a cold": "The common cold is a viral infection of your upper respiratory tract.",
    "what is flu": "Flu is a contagious respiratory illness caused by influenza viruses.",
    "what is asthma": "Asthma is a condition that affects the airways in your lungs, making them swollen and narrow, which makes it difficult to breathe.",
    "what is depression": "Depression is a mood disorder that causes persistent feelings of sadness and loss of interest in activities.",
    "what is anxiety": "Anxiety is a feeling of worry, nervousness, or unease about something with an uncertain outcome.",
    "what is a balanced diet": "A balanced diet includes a variety of foods from all food groups in the right proportions to maintain health and energy.",
    "what is cholesterol": "Cholesterol is a waxy substance found in the blood, and high levels can increase the risk of heart disease.",
    "what is obesity": "Obesity is a condition characterized by excessive body fat that can increase the risk of various health problems.",
    "what is a stroke": "A stroke occurs when blood flow to the brain is interrupted, causing brain cells to die and leading to potential brain damage.",
    "what is epilepsy": "Epilepsy is a neurological disorder characterized by recurrent seizures due to abnormal brain activity.",
    "what is schizophrenia": "Schizophrenia is a serious mental illness that affects how a person thinks, feels, and behaves.",
    "what is Alzheimer's disease": "Alzheimer's disease is a progressive neurodegenerative disorder that affects memory and cognitive function.",
    "what is a heart attack": "A heart attack occurs when blood flow to a part of the heart is blocked, causing damage to the heart muscle.",
    "what is a pacemaker": "A pacemaker is a small device implanted to help regulate heartbeats for people with heart arrhythmias.",
    "what is a CT scan": "A CT scan (computed tomography scan) is a medical imaging technique used to get detailed images of internal organs and structures.",
    "what is an MRI": "An MRI (Magnetic Resonance Imaging) is a diagnostic procedure that uses strong magnets and radio waves to create detailed images of organs and tissues.",
    "what is a blood test": "A blood test is a laboratory test used to check for the presence of disease markers, infection, and other health conditions.",
    "what is mental health": "Mental health refers to emotional, psychological, and social well-being. It affects how we think, feel, and act.",
    "what is a headache": "A headache is a pain or discomfort in the head or face area. It can be caused by various factors like tension, dehydration, or sinus issues.",
    "what is a fever": "A fever is a temporary increase in body temperature, often due to an infection or illness.",
    "what is arthritis": "Arthritis is a condition that causes inflammation and pain in the joints, with osteoarthritis and rheumatoid arthritis being the most common types.",
    "what is a mammogram": "A mammogram is an X-ray image of the breast used to detect early signs of breast cancer.",
    "what is a pap smear": "A pap smear is a screening test for cervical cancer, involving collecting cells from the cervix.",
    "what is cancer screening": "Cancer screening is the process of testing individuals for early signs of cancer before they show symptoms.",
    "what is a kidney stone": "A kidney stone is a hard deposit made of minerals and salts that form in the kidneys and can cause severe pain when passing.",
    "what is a protein supplement": "A protein supplement is a nutritional product used to increase protein intake, often used by athletes or those with dietary restrictions.",
    "what is a dental implant": "A dental implant is a surgical procedure to replace a missing tooth with a titanium post and artificial tooth.",
    "what is osteoporosis": "Osteoporosis is a condition that weakens bones, making them fragile and more likely to break.",
    "what is insomnia": "Insomnia is a sleep disorder characterized by difficulty falling asleep or staying asleep.",
    "what is ADHD": "ADHD (Attention Deficit Hyperactivity Disorder) is a neurodevelopmental disorder characterized by inattention, hyperactivity, and impulsivity.",
    "what is a blood pressure monitor": "A blood pressure monitor is a device used to measure blood pressure, typically at home or in a healthcare setting.",
    "what is pneumonia": "Pneumonia is an infection that causes inflammation in the air sacs of the lungs, which may fill with fluid or pus.",
    "what is multiple sclerosis": "Multiple sclerosis is an autoimmune disease that affects the central nervous system, leading to symptoms like numbness, weakness, and vision problems.",
    "what is a thyroid": "The thyroid is a butterfly-shaped gland in the neck that produces hormones responsible for regulating metabolism and energy.",
    "what is asthma management": "Asthma management includes using prescribed inhalers, avoiding triggers, and monitoring symptoms to control asthma attacks.",
    "what is a colonoscopy": "A colonoscopy is a procedure that examines the inside of the colon for abnormalities, such as polyps or cancer.",
    "what is a vaccine": "A vaccine is a biological preparation that provides immunity to a specific disease by stimulating the immune system.",
    "what is an allergy": "An allergy is an immune system reaction to substances that are typically harmless, such as pollen, pet dander, or certain foods.",
    "what is a dietitian": "A dietitian is a healthcare professional who specializes in nutrition and can help you make healthy food choices.",
    "what is a protein deficiency": "A protein deficiency occurs when the body doesn't get enough protein, which can lead to muscle wasting, weakness, and immune system issues.",
    "what is Parkinson's disease": "Parkinson's disease is a neurodegenerative disorder that affects movement, causing symptoms like tremors, stiffness, and balance problems.",
    "what is diabetes type 1": "Diabetes type 1 is an autoimmune disease where the body's immune system attacks the insulin-producing cells in the pancreas.",
    "what is diabetes type 2": "Diabetes type 2 is a condition where the body becomes resistant to insulin or doesn't produce enough insulin, leading to high blood sugar levels.",
    "what is hyperthyroidism": "Hyperthyroidism is a condition where the thyroid gland overproduces thyroid hormones, leading to symptoms like weight loss, rapid heartbeat, and anxiety.",
    "what is hypothyroidism": "Hypothyroidism is a condition where the thyroid produces insufficient amounts of thyroid hormones, leading to symptoms like fatigue, weight gain, and depression.",
    "what is a heart murmur": "A heart murmur is an unusual sound heard during a heartbeat, often caused by turbulent blood flow.",
    "what is cholesterol screening": "Cholesterol screening is a blood test used to measure the levels of cholesterol in the body, helping to assess the risk of heart disease.",
    "what is a urologist": "A urologist is a doctor who specializes in diagnosing and treating urinary tract diseases and male reproductive system issues.",
    "what is a cardiologist": "A cardiologist is a doctor who specializes in diagnosing and treating heart and blood vessel disorders.",
    "what is a neurologist": "A neurologist is a doctor who specializes in diagnosing and treating disorders of the nervous system, including the brain, spine, and nerves.",
    "what is a dermatologist": "A dermatologist is a doctor who specializes in diagnosing and treating skin conditions.",
    "what is a pediatrician": "A pediatrician is a doctor who specializes in the care of infants, children, and adolescents.",
    "what is a surgeon": "A surgeon is a medical professional who specializes in performing surgeries to treat diseases, injuries, or deformities.",
    "what is an optometrist": "An optometrist is a healthcare professional who specializes in vision care, including eye exams, prescribing glasses, and diagnosing eye conditions.",
    "what is an oncologist": "An oncologist is a doctor who specializes in diagnosing and treating cancer.",
    "what is an audiologist": "An audiologist is a healthcare professional who specializes in diagnosing and treating hearing and balance disorders.",
    "what is a pulmonologist": "A pulmonologist is a doctor who specializes in diagnosing and treating lung conditions, such as asthma, pneumonia, and COPD.",
    "what is a gastroenterologist": "A gastroenterologist is a doctor who specializes in diagnosing and treating disorders of the digestive system.",
    "what is a nephrologist": "A nephrologist is a doctor who specializes in diagnosing and treating kidney-related conditions.",
    "what is a rheumatologist": "A rheumatologist is a doctor who specializes in diagnosing and treating conditions affecting the joints, muscles, and bones, such as arthritis.",
    "what is a hematologist": "A hematologist is a doctor who specializes in diagnosing and treating blood disorders, including anemia and leukemia.",
    "what is a chiropractor": "A chiropractor is a healthcare professional who focuses on diagnosing and treating musculoskeletal disorders, particularly those related to the spine.",
    "what is a nutritionist": "A nutritionist is a specialist who provides guidance on diet and nutrition to help improve health and manage diseases.",
    "what is a podiatrist": "A podiatrist is a doctor who specializes in diagnosing and treating conditions of the feet and ankles.",
    "what is a speech therapist": "A speech therapist is a healthcare professional who helps individuals with speech, language, and swallowing disorders.",
    "what is a plastic surgeon": "A plastic surgeon specializes in reconstructive or cosmetic surgery to improve appearance or restore function.",
    "what is an obstetrician": "An obstetrician is a doctor who specializes in pregnancy, childbirth, and the postpartum period.",
    "what is a gynecologist": "A gynecologist is a doctor who specializes in women's reproductive health.",
    "what is a family doctor": "A family doctor provides primary care for individuals of all ages, from children to adults.",
    "what is a pain management specialist": "A pain management specialist focuses on diagnosing and treating chronic pain conditions.",
    "what is a sleep specialist": "A sleep specialist is a healthcare professional who diagnoses and treats sleep disorders, such as insomnia and sleep apnea.",
    "what is a wellness clinic": "A wellness clinic focuses on preventive healthcare and promoting overall well-being, often through lifestyle changes and holistic treatments.",
    "what is a weight loss clinic": "A weight loss clinic specializes in helping individuals lose weight and maintain a healthy body mass through medical guidance and programs."
},
    "why": {
        "why is healthcare important": "Healthcare is important because it promotes well-being, prevents disease, and provides the necessary treatments when health issues arise.",
    "why is hypertension dangerous": "Hypertension is dangerous because it can lead to serious complications like heart disease, stroke, and kidney damage if left untreated.",
    "why is diabetes a concern": "Diabetes is a concern because it can lead to long-term complications such as kidney failure, blindness, heart disease, and nerve damage.",
    "why does cancer occur": "Cancer occurs when abnormal cells in the body grow uncontrollably, often due to mutations in the DNA caused by environmental or genetic factors.",
    "why do people get the flu": "People get the flu because the influenza virus spreads through droplets from coughing, sneezing, or contact with contaminated surfaces.",
    "why does asthma happen": "Asthma occurs when the airways become inflamed and narrowed, making it difficult to breathe. It is often triggered by allergens, exercise, or cold air.",
    "why do we need a balanced diet": "A balanced diet is essential because it provides the necessary nutrients and energy to maintain optimal health and prevent nutritional deficiencies.",
    "why is depression common": "Depression is common due to a combination of factors such as genetics, chemical imbalances in the brain, life stressors, and environmental factors.",
    "why do people feel anxious": "People feel anxious when they experience a sense of worry or unease, often due to stressful situations, fear, or chemical imbalances in the brain.",
    "why is cholesterol important": "Cholesterol is important because it helps in the production of hormones, vitamin D, and bile acids. However, too much cholesterol can increase the risk of heart disease.",
    "why does obesity happen": "Obesity happens when the body stores excess fat, often due to a combination of factors such as poor diet, lack of exercise, genetics, and environmental influences.",
    "why is a stroke life-threatening": "A stroke is life-threatening because it disrupts the flow of blood to the brain, leading to brain damage and potentially causing loss of critical bodily functions.",
    "why does epilepsy occur": "Epilepsy occurs when there is abnormal electrical activity in the brain, which leads to recurrent seizures. Causes can include genetics, brain injury, or infections.",
    "why is schizophrenia hard to manage": "Schizophrenia is hard to manage because it involves a combination of hallucinations, delusions, and cognitive issues, which can be challenging to treat and control.",
    "why is Alzheimer's disease progressive": "Alzheimer's disease is progressive because it involves the gradual breakdown of brain cells, leading to memory loss, cognitive decline, and eventual loss of bodily functions.",
    "why does a heart attack happen": "A heart attack occurs when a coronary artery becomes blocked, restricting blood flow to the heart muscle, which causes tissue damage or death.",
    "why do some people need pacemakers": "Pacemakers are needed by people who have irregular heart rhythms (arrhythmias) to help regulate the heart's electrical signals and maintain normal heart function.",
    "why is a CT scan used": "A CT scan is used to obtain detailed images of internal organs and structures in the body, helping doctors diagnose conditions like tumors, injuries, and infections.",
    "why is an MRI more detailed than a CT scan": "An MRI is more detailed than a CT scan because it uses magnetic fields and radio waves to produce high-resolution images of soft tissues, whereas CT scans are better for visualizing bones.",
    "why do we get headaches": "Headaches occur due to various factors, including tension, stress, dehydration, lack of sleep, or underlying medical conditions like migraines or sinusitis.",
    "why is mental health important": "Mental health is important because it affects how we think, feel, and behave, and influences how we handle stress, relate to others, and make decisions.",
    "why is a blood test necessary": "A blood test is necessary to check for underlying health conditions, assess organ function, and monitor the levels of substances such as glucose, cholesterol, and red blood cells.",
    "why does arthritis cause pain": "Arthritis causes pain because it leads to inflammation in the joints, which can make movement difficult and result in discomfort and swelling.",
    "why is a mammogram important": "A mammogram is important because it helps detect early signs of breast cancer, allowing for early intervention and better treatment outcomes.",
    "why do we need cancer screenings": "Cancer screenings are important because they can detect cancer early when treatment is most effective, even before symptoms develop.",
    "why do kidney stones form": "Kidney stones form when minerals and salts in the urine crystallize and clump together, leading to the formation of hard deposits that can cause pain when passing.",
    "why should we take protein supplements": "Protein supplements are used to help individuals meet their daily protein needs, especially for athletes or those with dietary restrictions.",
    "why do people need dental implants": "Dental implants are needed to replace missing teeth and restore function, appearance, and confidence, as well as prevent bone loss in the jaw.",
    "why is osteoporosis common in older adults": "Osteoporosis is common in older adults due to the loss of bone density that occurs with age, making bones weaker and more susceptible to fractures.",
    "why is insomnia a problem": "Insomnia is a problem because it can lead to poor sleep quality, resulting in fatigue, mood disturbances, and impaired cognitive function during the day.",
    "why is ADHD often diagnosed in children": "ADHD is often diagnosed in children because they may exhibit symptoms of inattention, hyperactivity, and impulsivity that interfere with school and daily life activities.",
    "why is blood pressure monitoring necessary": "Blood pressure monitoring is necessary to track whether blood pressure is within a healthy range, as high blood pressure can lead to heart disease, stroke, and kidney problems.",
    "why do people get pneumonia": "Pneumonia is caused by infections, often bacterial or viral, that inflame the lungs, leading to symptoms like cough, fever, and difficulty breathing.",
    "why is multiple sclerosis difficult to treat": "Multiple sclerosis is difficult to treat because it is an autoimmune disease that attacks the protective covering of nerve fibers, leading to progressive neurological symptoms.",
    "why does the thyroid affect metabolism": "The thyroid affects metabolism because it produces hormones that regulate how the body uses energy, affecting weight, temperature regulation, and overall metabolism.",
    "why is asthma management important": "Asthma management is important to prevent asthma attacks, improve breathing, and enhance quality of life by controlling symptoms and reducing airway inflammation.",
    "why do we need colonoscopies": "Colonoscopies are needed to detect early signs of colorectal cancer or other conditions like polyps, which can be removed before they develop into cancer.",
    "why are vaccines important": "Vaccines are important because they protect against preventable diseases by stimulating the immune system to produce antibodies and build immunity.",
    "why do allergies occur": "Allergies occur when the immune system reacts to substances that are usually harmless, like pollen, pet dander, or certain foods.",
    "why is a dietitian important": "A dietitian is important because they provide expert advice on nutrition and meal planning, helping individuals achieve and maintain a healthy diet tailored to their needs.",
    "why do people suffer from protein deficiencies": "Protein deficiencies occur when the body does not get enough protein, leading to muscle weakness, fatigue, and immune system problems.",
    "why is Parkinson's disease progressive": "Parkinson's disease is progressive because it involves the gradual degeneration of dopamine-producing neurons in the brain, leading to worsening symptoms over time.",
    "why do people develop type 1 diabetes": "Type 1 diabetes occurs when the body's immune system mistakenly attacks and destroys the insulin-producing cells in the pancreas, leading to high blood sugar levels.",
    "why is type 2 diabetes more common than type 1": "Type 2 diabetes is more common than type 1 because it is associated with lifestyle factors such as obesity, poor diet, and lack of exercise.",
    "why do some people get hyperthyroidism": "Hyperthyroidism occurs when the thyroid produces excessive amounts of thyroid hormones, leading to symptoms such as rapid heartbeat, weight loss, and anxiety.",
    "why do some people develop hypothyroidism": "Hypothyroidism occurs when the thyroid gland does not produce enough thyroid hormones, leading to symptoms like fatigue, weight gain, and depression.",
    "why is a heart murmur concerning": "A heart murmur is concerning because it can indicate underlying heart conditions such as valve problems or congenital heart defects that may require treatment.",
    "why is cholesterol screening important": "Cholesterol screening is important because high cholesterol levels can lead to the development of heart disease and increase the risk of heart attacks or strokes.",
    "why do some people see urologists": "People see urologists for issues related to the urinary system, including conditions like kidney stones, urinary tract infections, and prostate problems.",
    "why do people see cardiologists": "People see cardiologists for heart-related conditions such as arrhythmias, heart disease, high blood pressure, and other cardiovascular issues.",
    "why do people need neurologists": "Neurologists are needed for diagnosing and treating conditions that affect the nervous system, such as migraines, epilepsy, and multiple sclerosis.",
    "why do we need dermatologists": "Dermatologists are needed for skin-related conditions, including acne, eczema, psoriasis, and skin cancer detection and treatment.",
    "why do we need pediatricians": "Pediatricians are needed to provide healthcare for children, ensuring their growth, development, and prevention of childhood illnesses.",
    "why do we need surgeons": "Surgeons are needed to perform surgical procedures to treat injuries, diseases, or conditions that cannot be managed with non-surgical treatments.",
    "why do we need optometrists": "Optometrists are needed to provide eye exams, prescribe corrective lenses, and diagnose and manage eye conditions like glaucoma and cataracts.",
    "why do we need oncologists": "Oncologists are needed to diagnose, treat, and manage cancer, offering treatments like chemotherapy, radiation, and surgery for various types of cancer.",
    "why do we need audiologists": "Audiologists are needed to diagnose and treat hearing disorders and balance problems, helping individuals improve their quality of life through hearing aids or therapy.",
    "why do we need pulmonologists": "Pulmonologists are needed for respiratory conditions like asthma, COPD, pneumonia, and other lung diseases.",
    "why do we need gastroenterologists": "Gastroenterologists are needed to diagnose and treat conditions affecting the digestive system, such as ulcers, acid reflux, and liver diseases.",
    "why do we need nephrologists": "Nephrologists are needed to diagnose and treat kidney-related conditions, including kidney disease, kidney stones, and dialysis management.",
    "why do we need rheumatologists": "Rheumatologists are needed for conditions affecting the joints and connective tissue, such as arthritis, lupus, and autoimmune disorders.",
    "why do we need hematologists": "Hematologists are needed to treat blood disorders such as anemia, leukemia, and clotting issues.",
    "why do we need chiropractors": "Chiropractors are needed to treat musculoskeletal issues, particularly back and neck pain, through spinal adjustments and other therapies.",
    "why do we need nutritionists": "Nutritionists are needed to offer dietary guidance and advice on healthy eating habits to help manage health conditions or improve overall well-being.",
    "why do we need podiatrists": "Podiatrists are needed to treat foot and ankle problems, including injuries, infections, and conditions like bunions or plantar fasciitis.",
    "why do we need speech therapists": "Speech therapists are needed to assist individuals with speech, language, and swallowing disorders, helping them improve communication and daily function."
},
    "where": {
       "where is the heart located": "The heart is located in the chest, slightly left of the center, behind the sternum and between the lungs.",
    "where is the liver located": "The liver is located in the upper right side of the abdomen, just below the diaphragm.",
    "where is the pancreas located": "The pancreas is located behind the stomach, extending horizontally across the back of the abdomen.",
    "where is the brain located": "The brain is located within the skull, encased in the cranium, and controls most functions of the body.",
    "where is the spinal cord located": "The spinal cord runs down the back, inside the vertebral column, and is responsible for transmitting nerve signals between the brain and body.",
    "where is the thyroid gland located": "The thyroid gland is located in the neck, just below the Adam's apple, and controls metabolism through hormone production.",
    "where is the gallbladder located": "The gallbladder is located under the liver, in the upper right side of the abdomen.",
    "where is the bladder located": "The bladder is located in the lower abdomen, behind the pubic bone, and stores urine until it is excreted.",
    "where is the small intestine located": "The small intestine is located in the central and lower abdomen, and it is responsible for digestion and absorption of nutrients.",
    "where is the large intestine located": "The large intestine is located around the perimeter of the abdominal cavity, surrounding the small intestine, and is responsible for absorbing water and electrolytes.",
    "where do you get a flu shot": "You can get a flu shot at healthcare providers' offices, pharmacies, community health centers, and clinics.",
    "where do you get a COVID-19 vaccine": "You can get a COVID-19 vaccine at hospitals, clinics, pharmacies, and designated vaccination centers.",
    "where is the liver most vulnerable": "The liver is most vulnerable to damage from alcohol consumption, viral infections (like hepatitis), and exposure to toxins.",
    "where are kidneys located": "The kidneys are located in the lower back, one on each side of the spine, just below the rib cage.",
    "where is the appendix located": "The appendix is located in the lower right side of the abdomen, attached to the large intestine.",
    "where does blood flow after the heart": "After the heart, blood flows through the arteries to various parts of the body, delivering oxygen and nutrients.",
    "where are white blood cells produced": "White blood cells are primarily produced in the bone marrow, though they also mature in lymphatic tissues like the spleen and lymph nodes.",
    "where can you get a blood test": "You can get a blood test at a healthcare provider’s office, laboratory, or hospital.",
    "where does digestion begin": "Digestion begins in the mouth, where food is broken down by chewing and enzymes in saliva.",
    "where are antibiotics used": "Antibiotics are used to treat bacterial infections, such as respiratory infections, skin infections, urinary tract infections, and more.",
    "where can I find a neurologist": "Neurologists can be found in hospitals, clinics, and private practice offices specializing in brain and nervous system disorders.",
    "where can I find a cardiologist": "Cardiologists can be found in hospitals, heart centers, and private practice offices specializing in heart health.",
    "where is the best place to get a COVID test": "COVID-19 tests are available at hospitals, clinics, pharmacies, and specific drive-through testing sites.",
    "where do children get their vaccines": "Children can receive vaccines at pediatricians' offices, community health centers, and public health clinics.",
    "where is the best place to get mental health counseling": "Mental health counseling is available through therapists’ offices, hospitals, community mental health centers, and online therapy services.",
    "where can I get a mammogram": "Mammograms are available at hospitals, breast health centers, and radiology clinics.",
    "where is the best place to get a colonoscopy": "Colonoscopies are typically performed at hospitals, outpatient surgical centers, and gastroenterology clinics.",
    "where can I get a dental cleaning": "Dental cleanings are available at dentist's offices, usually during routine check-ups.",
    "where do vaccines come from": "Vaccines are developed by pharmaceutical companies and research institutions and are then distributed to healthcare providers and clinics.",
    "where can I donate blood": "You can donate blood at local blood banks, hospitals, or through organizations like the Red Cross.",
    "where can I find an oncologist": "Oncologists can be found in hospitals, cancer treatment centers, and private practices specializing in cancer care.",
    "where can I find an optometrist": "Optometrists are available in optometry clinics, optical stores, and private practice offices, where they conduct eye exams and prescribe glasses.",
    "where is cholesterol found": "Cholesterol is found in animal-based foods like meat, dairy products, and eggs, and is also produced by the liver.",
    "where does your body store fat": "Fat is stored in fat cells, located throughout the body, primarily in the abdominal area, thighs, and buttocks.",
    "where do you get an MRI": "An MRI can be performed at hospitals, diagnostic imaging centers, or outpatient medical facilities.",
    "where is the best place for physiotherapy": "Physiotherapy is available at physiotherapy clinics, hospitals, rehabilitation centers, and sports medicine centers.",
    "where do people with allergies go for treatment": "People with allergies can seek treatment from allergists, who work in private practices, hospitals, and specialized allergy clinics.",
    "where is the best place to get a flu vaccine": "The flu vaccine can be received at doctor’s offices, pharmacies, and public health clinics.",
    "where do people get a hearing test": "Hearing tests are conducted at audiology clinics, hospitals, or ENT (Ear, Nose, Throat) specialist offices.",
    "where can I find a dietitian": "Dietitians can be found in hospitals, private practices, and outpatient clinics, specializing in nutrition counseling.",
    "where can I go to get an ECG": "An ECG (electrocardiogram) can be performed in hospitals, cardiology clinics, and outpatient centers.",
    "where do people go for eye exams": "Eye exams are typically available at optometrists' offices, ophthalmologist clinics, and optical stores.",
    "where can I find a pulmonologist": "Pulmonologists can be found in hospitals, pulmonary medicine clinics, and private practices that specialize in lung health.",
    "where do we get vaccines from": "Vaccines are developed and distributed by pharmaceutical companies and health authorities, and are given in clinics, hospitals, and pharmacies.",
    "where can I find a rheumatologist": "Rheumatologists can be found in hospitals, private practices, and specialized rheumatology clinics that treat conditions like arthritis.",
    "where are newborns vaccinated": "Newborns are vaccinated at pediatricians' offices, hospitals, and community health centers.",
    "where can I find a dermatologist": "Dermatologists can be found in dermatology clinics, private practice offices, and hospitals.",
    "where do we go for allergy testing": "Allergy testing is available at allergy clinics, dermatology offices, and some hospitals or general practices.",
    "where can I find a podiatrist": "Podiatrists can be found in podiatry clinics, private practices, and hospitals, specializing in foot and ankle care.",
    "where do we get dialysis": "Dialysis is typically done at dialysis centers, hospitals, and some specialized clinics for individuals with kidney failure.",
    "where can I find a gastroenterologist": "Gastroenterologists can be found in gastroenterology clinics, hospitals, and private practice offices specializing in digestive health.",
    "where can I get an X-ray": "X-rays are available at hospitals, imaging centers, and outpatient clinics specializing in diagnostic radiology.",
    "where can I go for an ultrasound": "Ultrasounds can be performed at hospitals, imaging centers, and outpatient clinics.",
    "where can I get a dental implant": "Dental implants are typically placed by oral surgeons or dentists at dental offices or specialized implant centers.",
    "where can I get a pregnancy test": "Pregnancy tests are available at pharmacies, clinics, and doctor’s offices.",
    "where can I get a tetanus shot": "Tetanus shots are available at doctor’s offices, pharmacies, and public health clinics.",
    "where can I find an orthopedic surgeon": "Orthopedic surgeons can be found in orthopedic clinics, hospitals, and private practice offices specializing in musculoskeletal care.",
    "where can I find a urologist": "Urologists can be found in hospitals, urology clinics, and private practices specializing in the urinary system and male reproductive health.",
    "where can I get a prostate exam": "Prostate exams are available at urologists' offices, primary care doctor’s offices, and specialized clinics.",
    "where do I get tested for HIV": "HIV testing is available at clinics, hospitals, specialized HIV/AIDS centers, and sometimes at public health organizations.",
    "where is cancer treated": "Cancer treatment is available at cancer centers, hospitals, and specialized oncology clinics.",
    "where can I get a health checkup": "Health checkups can be done at primary care doctor’s offices, health clinics, and hospitals.",
    "where do I find an immunologist": "Immunologists can be found in specialized clinics, hospitals, and private practices treating immune system disorders.",
    "where is the best place to get a skin biopsy": "Skin biopsies are typically done at dermatology clinics, hospitals, or by a healthcare professional specializing in skin conditions.",
    "where can I get physical therapy": "Physical therapy is available at physical therapy clinics, hospitals, rehabilitation centers, and outpatient clinics.",
    "where is the best place to get a vaccine passport": "Vaccine passports are typically issued through health authorities or government agencies in your country, or digitally via health apps.",
    "where is the best place to get mental health therapy": "Mental health therapy is available through licensed therapists, psychologists, and counselors in private practice or through hospitals and clinics.",
    "where is the best place to get a cervical smear": "Cervical smears (Pap smears) can be done at gynecologists' offices, health clinics, and some primary care doctor’s offices.",
    "where do I go for pain management": "Pain management specialists can be found in pain clinics, hospitals, and outpatient centers that offer treatments for chronic pain."
},
    "how": {
        "how to cure a cold": "The common cold is caused by viruses and usually resolves on its own. Rest, hydration, and over-the-counter medications for symptom relief are often helpful.",
    "how to cure a headache": "Headaches can be treated with over-the-counter pain relievers like ibuprofen or acetaminophen, staying hydrated, and rest. If persistent, see a doctor.",
    "how to cure a sore throat": "A sore throat can be treated with warm saltwater gargles, throat lozenges, over-the-counter pain relievers, and staying hydrated.",
    "how to cure acne": "Acne can be treated with topical creams containing benzoyl peroxide or salicylic acid, and sometimes antibiotics or oral medication. A dermatologist can provide tailored treatment.",
    "how to cure insomnia": "Insomnia can be managed with good sleep hygiene, such as maintaining a regular sleep schedule, avoiding caffeine, and using relaxation techniques. In some cases, medication may be prescribed.",
    "how to cure a cough": "Coughs are usually caused by viral infections, and over-the-counter cough medicines, honey, and staying hydrated can help relieve symptoms. If persistent, consult a doctor.",
    "how to cure indigestion": "Indigestion can be treated with antacids, proton pump inhibitors, or lifestyle changes such as eating smaller meals and avoiding spicy foods.",
    "how to cure nausea": "Nausea can be alleviated by drinking ginger tea, staying hydrated, and taking anti-nausea medication as recommended by a doctor.",
    "how to cure a sprained ankle": "Rest, ice, compression, and elevation (R.I.C.E.) are commonly recommended for treating a sprained ankle. Over-the-counter pain relievers may help reduce inflammation and pain.",
    "how to cure an upset stomach": "An upset stomach can be treated with antacids, staying hydrated, avoiding heavy foods, and taking over-the-counter medications like Pepto-Bismol or Imodium if necessary.",
    "how to cure high blood pressure": "High blood pressure can be managed with lifestyle changes, such as exercise, a healthy diet, stress management, and medications like ACE inhibitors or diuretics.",
    "how to cure anxiety": "Anxiety can be managed with therapy (such as cognitive-behavioral therapy), relaxation techniques, and medications like SSRIs or benzodiazepines, as prescribed by a doctor.",
    "how to cure depression": "Depression can be treated with therapy, such as cognitive-behavioral therapy or antidepressant medications, like SSRIs or SNRIs, prescribed by a healthcare provider.",
    "how to cure a burn": "Minor burns can be treated by cooling the area with cold water, applying aloe vera gel, and using over-the-counter pain relievers. Severe burns require immediate medical attention.",
    "how to cure a mosquito bite": "Mosquito bites can be treated with antihistamine creams, hydrocortisone, or a cool compress to relieve itching and swelling.",
    "how to cure a fever": "Fever can be treated with rest, fluids, and fever-reducing medications like acetaminophen or ibuprofen. If the fever is high or persistent, seek medical advice.",
    "how to cure a muscle cramp": "Muscle cramps can be relieved by stretching the affected muscle, massaging it, staying hydrated, and taking over-the-counter pain relievers.",
    "how to cure constipation": "Constipation can be treated by increasing fiber intake, staying hydrated, exercising, and using over-the-counter laxatives if necessary.",
    "how to cure a toothache": "Toothaches can be alleviated with over-the-counter pain relievers, warm saltwater rinses, and applying cold compresses. A dentist should be consulted if pain persists.",
    "how to cure an ear infection": "Ear infections can be treated with antibiotics if bacterial, or with pain relievers and warm compresses if viral. See a doctor for appropriate treatment.",
    "how to cure nausea during pregnancy": "Nausea during pregnancy can be managed with ginger, vitamin B6 supplements, and eating smaller meals throughout the day. Consult a healthcare provider for safe treatment options.",
    "how to cure a cough during pregnancy": "During pregnancy, a cough can be managed with honey, ginger tea, or over-the-counter medications recommended by a healthcare provider. Always consult your doctor first.",
    "how to cure a urinary tract infection": "A urinary tract infection (UTI) is typically treated with antibiotics. It's important to complete the prescribed course of medication and stay hydrated.",
    "how to cure allergies": "Allergies can be managed with antihistamines, nasal sprays, and avoiding allergens. For severe cases, allergy shots or immunotherapy may be recommended by an allergist.",
    "how to cure chickenpox": "Chickenpox is typically treated with calamine lotion, antihistamines, and fever-reducing medications. Vaccination can prevent chickenpox in the future.",
    "how to cure bronchitis": "Bronchitis can be treated with rest, fluids, cough suppressants, and sometimes antibiotics if it’s bacterial. A doctor may prescribe medications to ease symptoms.",
    "how to cure pneumonia": "Pneumonia is typically treated with antibiotics if bacterial, and antiviral medications if viral. Hospitalization may be required for severe cases.",
    "how to cure a cold sore": "Cold sores can be treated with antiviral creams or oral antiviral medications. Over-the-counter pain relievers and ice packs can also help alleviate discomfort.",
    "how to cure a tooth infection": "A tooth infection may require a dental visit for drainage and antibiotics. Over-the-counter pain relievers can help with discomfort in the meantime.",
    "how to cure a headache naturally": "Natural treatments for headaches include applying cold or warm compresses, drinking water, practicing relaxation techniques, and using essential oils like peppermint or lavender.",
    "how to cure a hangover": "Hangovers can be alleviated by drinking water, eating a balanced meal, taking over-the-counter pain relievers, and getting plenty of rest.",
    "how to cure asthma": "Asthma can be managed with inhalers (bronchodilators and corticosteroids), avoiding triggers, and maintaining a healthy lifestyle. A doctor will create an asthma management plan.",
    "how to cure a panic attack": "Panic attacks can be managed with relaxation techniques, deep breathing exercises, and, in some cases, anti-anxiety medications prescribed by a doctor.",
    "how to cure heartburn": "Heartburn can be treated with antacids, proton pump inhibitors (PPIs), and avoiding foods and habits that trigger acid reflux.",
    "how to cure a back pain": "Back pain can be managed with rest, physical therapy, over-the-counter pain relievers, hot or cold compresses, and proper posture.",
    "how to cure vertigo": "Vertigo can be treated with medications to alleviate dizziness, vestibular therapy, and in some cases, balance exercises or procedures performed by a healthcare provider.",
    "how to cure a sinus infection": "A sinus infection can be treated with decongestants, nasal saline rinses, and sometimes antibiotics if it's bacterial.",
    "how to cure psoriasis": "Psoriasis can be treated with topical corticosteroids, light therapy, and systemic medications in severe cases. A dermatologist can provide personalized treatment.",
    "how to cure eczema": "Eczema can be treated with moisturizing creams, corticosteroid ointments, and avoiding triggers like harsh soaps or allergens.",
    "how to cure arthritis": "Arthritis can be treated with pain relievers, physical therapy, joint protection techniques, and medications to reduce inflammation.",
    "how to cure a urinary infection": "A urinary tract infection (UTI) is typically treated with antibiotics. Drink plenty of water and take all prescribed antibiotics to prevent recurrence.",
    "how to cure a swollen ankle": "A swollen ankle can be treated with rest, ice, compression, and elevation (R.I.C.E.). Pain relievers like ibuprofen can help reduce swelling.",
    "how to cure a fever naturally": "Fever can be managed with rest, staying hydrated, and using a cool compress. Avoid overdressing and drink plenty of fluids.",
    "how to cure a runny nose": "A runny nose can be treated with decongestants, saline nasal sprays, and staying hydrated. A humidifier can also help.",
    "how to cure a stomach ulcer": "Stomach ulcers can be treated with medications to reduce stomach acid (like proton pump inhibitors) and antibiotics if the ulcer is caused by an infection.",
    "how to cure insomnia naturally": "Natural treatments for insomnia include herbal teas (like chamomile), relaxation techniques, and avoiding caffeine or screen time before bed.",
    "how to cure a skin rash": "A skin rash can be treated with antihistamines, topical corticosteroids, or over-the-counter creams for itching and inflammation. See a doctor if the rash persists.",
    "how to cure a dry cough": "A dry cough can be treated with cough suppressants, staying hydrated, and using throat lozenges to soothe the throat.",
    "how to cure a fever in children": "Fever in children can be treated with fever-reducing medications like acetaminophen or ibuprofen (as recommended by a doctor), and ensuring they stay hydrated.",
    "how to cure a sore back": "Sore backs can be relieved with rest, hot or cold compresses, over-the-counter pain relievers, and exercises that strengthen the back muscles.",
    "how to cure a bruise": "Bruises can be treated with ice packs, rest, and elevation. Over-the-counter pain relievers may help if the bruise is painful.",
    "how to cure a stuffy nose": "A stuffy nose can be treated with saline nasal sprays, steam inhalation, decongestants, and keeping hydrated.",
    "how to cure high cholesterol": "High cholesterol can be managed with a healthy diet, exercise, and medications like statins prescribed by a healthcare provider.",
    "how to cure constipation naturally": "Constipation can be alleviated with a high-fiber diet, increased water intake, and regular exercise. Over-the-counter natural laxatives may also help.",
    "how to cure sciatica": "Sciatica can be treated with physical therapy, anti-inflammatory medications, stretching exercises, and sometimes epidural steroid injections.",
    "how to cure nausea after chemotherapy": "Nausea after chemotherapy can be managed with anti-nausea medications prescribed by a doctor, ginger, and dietary changes.",
    "how to cure a concussion": "Concussions require rest, avoiding strenuous physical activity, and monitoring for symptoms. A healthcare provider may give specific guidelines for recovery.",
    "how to cure fatigue": "Fatigue can be managed by ensuring proper sleep, maintaining a balanced diet, and managing stress. If persistent, consult a healthcare provider for further evaluation.",
    "how to cure a pinched nerve": "A pinched nerve can be treated with rest, physical therapy, anti-inflammatory medications, and, in some cases, surgery if the condition is severe.",
    "how to cure insomnia with meditation": "Meditation can be an effective natural remedy for insomnia by promoting relaxation and reducing stress. Guided sleep meditations may help improve sleep quality.",
    "how to cure asthma naturally": "Asthma can be managed with a healthy lifestyle, avoiding triggers, and sometimes using natural remedies like ginger or honey. Always follow your doctor’s treatment plan.",
    "how to cure vertigo naturally": "Vertigo can be managed with balance exercises, hydration, and vestibular rehabilitation therapy. Consult a doctor for personalized treatments.",
    "how to cure sinusitis": "Sinusitis can be treated with nasal saline rinses, decongestants, and sometimes antibiotics if the infection is bacterial."
}
    # Add more categories as needed
}

# Basic conversation responses
basic_conversations = {
    "hi": "Hello! How can I assist you today?",
    "hello": "Hi! How can I help you today?",
    "good morning": "Good morning! How can I assist you with healthcare today?",
    "good evening": "Good evening! How can I assist you today?",
    "who are you": "I am a healthcare chatbot here to help you with your health-related questions.",
    "how are you": "I'm just a bot, but I'm ready to assist you with any healthcare queries!",
    "bye": "Goodbye! Take care and stay healthy!",
    "thank you": "You're welcome! Let me know if you need more help.",
    "thanks": "You're welcome! I'm here to help.",
    "what's your name": "I'm your healthcare assistant bot, here to help you with health questions.",
    "how can i contact you": "You can always come back here and ask me anything related to health!",
    # Add more conversational inputs here
}

# Function to generate a response using fuzzy matching
def generate_response(user_input):
    user_input = user_input.lower()

    # Check if the user input matches a basic conversation response
    if user_input in basic_conversations:
        return basic_conversations[user_input]

    # Debug: Print the input to see what the bot is processing
    print(f"User Input: {user_input}")

    # Check healthcare categories (What, Why, Where, How)
    best_match_score = 0
    best_match_answer = None

    for category, qa_dict in healthcare_knowledge_base.items():
        for question, answer in qa_dict.items():
            # Perform fuzzy matching for each question in the category
            best_match, score = process.extractOne(user_input, [question])

            # Debug: Print the best match and score for each category
            print(f"Checking: {question} -> Match: {best_match}, Score: {score}")

            # Update if score is higher than the best match score found so far
            if score > best_match_score:
                best_match_score = score
                best_match_answer = answer

    # If the best match score is above a certain threshold, return the answer
    if best_match_score >= 70:
        return best_match_answer

    # If no match is found, respond with a generic message
    return "I'm sorry, I didn't understand that. Can you ask something else?"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json['message']
    response = generate_response(user_input)
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True)
