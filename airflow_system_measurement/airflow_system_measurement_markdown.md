<img src="airflow.png"/>
<div id="top"></div>

## Airflow system measurement
#### Content: 
  * <a href="#heavy_processing">Heavy processing</a>
  * <a href="#disable_multiple_triggers">Disable multiple triggers</a>
  * <a href="#metadata_for_production">Metadata for production</a>
  * <a href="#best_practices">Best practices</a>
    * <a href="#top_level_python_code">Top level python code</a>
    * <a href="#creating_a_task">Creating a task</a>
    * <a href="#dynamic_DAG_generation">Dynamic DAG generation</a>
    * <a href="#triggering_DAGs_after_changes">Triggering DAGs after changes</a>
    * <a href="#reducing_DAG_complexity">Reducing DAG complexity</a>


<p align="right">(<a href="#top">back to top</a>)</p>


  * ##### Always calculate Airflow worker node requirements.

<div id="light_docker"></div>

  * ##### Keep your airflow docker image light.
    Create the docker image with other libraries of airflow you required, remove the uncessary ones from official airflow, Example you are working on AWS then remove GCP, AZURE operators/libaries if available. Always keep the airflow docker image light in kubernetes environment, so that tasks can be executed on it from airflow worker node.

  

<div id="heavy_processing"></div>

  * ##### Heavy processing
    Do not do heavy processing on Airflow worker nodes, example: downloading TBs of data and analysis them on airflow worker. 
    Use 3rd party systems like Databricks/Spark, Snowflake, etc. Airflow is mainly used to create connections and execute tasks remotely. We can perform light tasks on airflow worker nodes. Light tasks which will occupy less CPU, Memory and Storage.

<div id="disable_multiple_triggers"></div>

  * ##### Disable multiple triggers
    while defining a DAG always keep "catchup"=False --> To disable multiple triggers (or disable backfilling)
    Example: Start Date: 1-1-2020, Schedule: daily, if catch up = True, Then there will be 450 dag runs.  
    It can increase load on airflow instances and cost. Make sure you use this feature by calculating your resources.

<div id="metadata_for_production"></div>

  * ##### Metadata for production
    Always use remote metadata for apache airflow in production.
    Example: Postgres (AWS RDS)
<p align="right">(<a href="#top">back to top</a>)</p>


<!-- Best Practices -->
<div id="best_practices"></div>

* ##### Best Practices
  <div id="top_level_python_code"></div>

    * ###### Top level Python Code
      Avoid writing the top level Python Code While dag development, always import additional libraries inside your python function called by python operator.

    <div id="creating_a_task"></div>

    * ###### Creating a task
        The Python datetime now() function gives the current datetime object.
        This function should never be used inside a task, especially to do the critical computation, as it leads to different outcomes on each run. It’s fine to use it, for example, to generate a temporary log.
        You should define repetitive parameters such as connection_id or S3 paths in default_args rather than declaring them for each task. 
        The default_args help to avoid mistakes such as typographical errors. 
    <div id="dynamic_DAG_generation"></div>

    * ###### Dynamic DAG generation
        Avoiding excessive processing at the top level code described in the previous chapter is especially important in case of dynamic DAG configuration, which can be configured essentially in one of those ways:
        * via environment variables (not to be mistaken with the Airflow Variables)
		* via externally provided, generated Python code, containing meta-data in the DAG folder
		* via externally provided, generated configuration meta-data file in the DAG folder
    
    <div id="triggering_DAGs_after_changes"></div>

    * ###### Triggering DAGs after changes
        Avoid triggering DAGs immediately after changing them or any other accompanying files that you change in the DAG folder.
        You should give the system sufficient time to process the changed files


