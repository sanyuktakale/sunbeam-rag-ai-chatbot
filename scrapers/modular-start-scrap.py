import modular_scrap_course as scraper

# List of courses to scrape
courses = [
    ("https://sunbeaminfo.in/modular-courses/apache-spark-mastery-data-engineering-pyspark", "Apache Spark Mastery", "apache_spark_mastery_scrap.pdf"),
    ("https://sunbeaminfo.in/modular-courses/core-java-classes", "Core Java Classes", "core_java_classes_scrap.pdf"),
    ("https://sunbeaminfo.in/modular-courses/aptitude-course-in-pune", "Aptitude", "Aptitude_Course_Details.pdf"),
    ("https://sunbeaminfo.in/modular-courses/data-structure-algorithms-using-java", "Data Structures and Algorithms", "data_structures_algorithms_scrap.pdf"),
    ("https://sunbeaminfo.in/modular-courses/Devops-training-institute", "Dev Ops", "dev_ops_scrap.pdf"),
    ("https://sunbeaminfo.in/modular-courses/dreamllm-training-institute-pune", "Dream LLM", "dream_llm_scrap.pdf"),
    ("https://sunbeaminfo.in/modular-courses/machine-learning-classes", "Machine Learning", "machine_learning_scrap.pdf"),
    ("https://sunbeaminfo.in/modular-courses/mastering-generative-ai", "Mastering Generative AI", "mastering_gen_ai_scrap.pdf"),
    ("https://sunbeaminfo.in/modular-courses.php?mdid=57", "Mastering MCQs", "mastering_mcqs_scrap.pdf"),
    ("https://sunbeaminfo.in/modular-courses/mern-full-stack-developer-course", "MERN Full Stack", "mern_full_stack_scrap.pdf"),
    ("https://sunbeaminfo.in/modular-courses/mlops-llmops-training-institute-pune", "MLOps & LLMOps", "mlops_llmops_scrap.pdf"),
    ("https://sunbeaminfo.in/modular-courses/python-classes-in-pune", "Python Development", "python_development_scrap.pdf")
]

# Loop through and scrape
for url, name, filename in courses:
    print(f"Starting: {name}")
    scraper.scrape_modular_courses(url, name, filename)
    print(f"Completed: {name}\n")