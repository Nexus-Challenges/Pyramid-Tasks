from fastapi import FastAPI, HTTPException
import psycopg2

CONN = psycopg2.connect(
        host="34.151.226.186",
        database="pyramid",
        user="pyramid",
        password="pyramid@234",
        port=3022)

cursor = CONN.cursor()

app = FastAPI()


@app.post('/tasks/create')
def create_task(request_name: str, request_description: str, request_icon: str, request_action: str):
    try:
        if len(request_name) > 2:
            consulta_sql = "INSERT INTO pyramid_tasks (task_name, task_description, task_icon, task_action) VALUES (%s, %s, %s, %s)"
            task = (request_name, request_description, request_icon, request_action)
            cursor.execute(consulta_sql, task)
            CONN.commit()

            return {'status': 'task criada com sucesso'}
    except Exception as e:
        return {'status': f'falha na criação da task: {str(e)}'}
    
@app.post('/tasks/delete')
def delete_task(task_id: int):
    try:
        task_delete = f"DELETE FROM pyramid_tasks WHERE task_id = {task_id}"
        cursor.execute(task_delete)
        CONN.commit()
        if cursor.rowcount > 0:
            return {'status': 'Task deletada com sucesso'}
        else:
            raise HTTPException(status_code=404, detail='Tarefa não encontrada')
    except Exception as e:
        return {'status': f'Erro ao deletar a task: {str(e)}'}
    

    
@app.get('/tasks/')
def view_tasks():
    try:
        consulta_sql = "SELECT * FROM pyramid_tasks"
        cursor.execute(consulta_sql)
        registros = cursor.fetchall()
        return {'status': 'sucesso', 'dados': registros}
    
    except Exception as e:
        return {'status': f'falha busca: {str(e)}'}
    

@app.get('/tasks/{task_id}')    
def view_tasks(task_id: int):
    try:
        consulta_sql = f"SELECT * FROM pyramid_tasks WHERE task_id = {task_id}"
        cursor.execute(consulta_sql)
        registros = cursor.fetchall()
        return {'status': 'sucesso', 'dados': registros}
    
    except Exception as e:
        return {'status': f'falha busca: {str(e)}'}




    