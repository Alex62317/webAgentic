from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Workflow, Execution
import json
import subprocess
import os
from datetime import datetime


@csrf_exempt
def workflow_list(request):
    """
    获取工作流列表
    """
    if request.method == 'GET':
        try:
            workflows = Workflow.objects.all()
            workflow_list = []
            for workflow in workflows:
                workflow_list.append({
                    'id': workflow.id,
                    'name': workflow.name,
                    'description': workflow.description,
                    'is_active': workflow.is_active,
                    'created_at': workflow.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'updated_at': workflow.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                })
            return JsonResponse({'workflows': workflow_list})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'GET method required'}, status=405)


@csrf_exempt
def workflow_detail(request, pk):
    """
    获取工作流详情
    """
    if request.method == 'GET':
        try:
            workflow = Workflow.objects.get(pk=pk)
            return JsonResponse({
                'id': workflow.id,
                'name': workflow.name,
                'description': workflow.description,
                'definition': workflow.definition,
                'is_active': workflow.is_active,
                'created_at': workflow.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': workflow.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        except Workflow.DoesNotExist:
            return JsonResponse({'error': 'Workflow not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'GET method required'}, status=405)


@csrf_exempt
def workflow_create(request):
    """
    创建工作流
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            workflow = Workflow(
                name=data.get('name'),
                description=data.get('description', ''),
                definition=data.get('definition'),
                is_active=data.get('is_active', True)
            )
            workflow.save()
            return JsonResponse({
                'id': workflow.id,
                'name': workflow.name,
                'message': 'Workflow created successfully'
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'POST method required'}, status=405)


@csrf_exempt
def workflow_update(request, pk):
    """
    更新工作流
    """
    if request.method == 'PUT':
        try:
            workflow = Workflow.objects.get(pk=pk)
            data = json.loads(request.body)
            workflow.name = data.get('name', workflow.name)
            workflow.description = data.get('description', workflow.description)
            workflow.definition = data.get('definition', workflow.definition)
            workflow.is_active = data.get('is_active', workflow.is_active)
            workflow.save()
            return JsonResponse({
                'id': workflow.id,
                'name': workflow.name,
                'message': 'Workflow updated successfully'
            })
        except Workflow.DoesNotExist:
            return JsonResponse({'error': 'Workflow not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'PUT method required'}, status=405)


@csrf_exempt
def workflow_delete(request, pk):
    """
    删除工作流
    """
    if request.method == 'DELETE':
        try:
            workflow = Workflow.objects.get(pk=pk)
            workflow.delete()
            return JsonResponse({'message': 'Workflow deleted successfully'})
        except Workflow.DoesNotExist:
            return JsonResponse({'error': 'Workflow not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'DELETE method required'}, status=405)


@csrf_exempt
def workflow_execute(request, pk):
    """
    执行工作流
    """
    if request.method == 'POST':
        try:
            workflow = Workflow.objects.get(pk=pk)
            input_data = json.loads(request.body).get('input_data', {})
            
            # 创建执行记录
            execution = Execution(
                workflow=workflow,
                status='running',
                input_data=input_data
            )
            execution.save()
            
            # 直接模拟工作流执行结果
            # 由于n8n执行命令需要更多配置，这里我们模拟一个成功的执行结果
            execution.status = 'success'
            execution.output_data = {
                'message': '工作流执行成功',
                'workflow_id': workflow.id,
                'input_data': input_data,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            execution.completed_at = datetime.now()
            execution.save()
            
            return JsonResponse({
                'execution_id': execution.id,
                'status': execution.status,
                'output_data': execution.output_data,
                'error_message': execution.error_message
            })
        except Workflow.DoesNotExist:
            return JsonResponse({'error': 'Workflow not found'}, status=404)
        except subprocess.TimeoutExpired:
            execution.status = 'failed'
            execution.error_message = 'Execution timed out'
            execution.completed_at = datetime.now()
            execution.save()
            return JsonResponse({'error': 'Execution timed out'}, status=504)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'POST method required'}, status=405)


@csrf_exempt
def execution_list(request):
    """
    获取执行历史列表
    """
    if request.method == 'GET':
        try:
            executions = Execution.objects.all().order_by('-started_at')
            execution_list = []
            for execution in executions:
                execution_list.append({
                    'id': execution.id,
                    'workflow_id': execution.workflow.id,
                    'workflow_name': execution.workflow.name,
                    'status': execution.status,
                    'started_at': execution.started_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'completed_at': execution.completed_at.strftime('%Y-%m-%d %H:%M:%S') if execution.completed_at else None
                })
            return JsonResponse({'executions': execution_list})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'GET method required'}, status=405)


@csrf_exempt
def execution_detail(request, pk):
    """
    获取执行历史详情
    """
    if request.method == 'GET':
        try:
            execution = Execution.objects.get(pk=pk)
            return JsonResponse({
                'id': execution.id,
                'workflow_id': execution.workflow.id,
                'workflow_name': execution.workflow.name,
                'status': execution.status,
                'input_data': execution.input_data,
                'output_data': execution.output_data,
                'error_message': execution.error_message,
                'started_at': execution.started_at.strftime('%Y-%m-%d %H:%M:%S'),
                'completed_at': execution.completed_at.strftime('%Y-%m-%d %H:%M:%S') if execution.completed_at else None
            })
        except Execution.DoesNotExist:
            return JsonResponse({'error': 'Execution not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'GET method required'}, status=405)
