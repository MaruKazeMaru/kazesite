from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from . import models

def get_title(url_name, kwargs=None):
	if url_name == 'index': return "トップ"
	elif url_name == 'about_original_system': return "元システムの概要"
	#建物関連
	elif url_name == 'list_building': return "建物一覧"
	elif url_name == 'create_building': return "建物登録"
	elif url_name == 'detail_building':
		if 'object' in kwargs:
			building = kwargs['object']
		else:
			building = get_object_or_404(models.Building, pk=kwargs['pk'])
		return "建物詳細:" + building.name
	elif url_name == 'delete_building':
		building = get_object_or_404(models.Building, pk=kwargs['pk'])
		return "建物情報削除:" + building.name
	elif url_name == 'update_building':
		building = get_object_or_404(models.Building, pk=kwargs['pk'])
		return "建物情報更新:" + building.name
	#温度計関連
	elif url_name == 'list_thermometer': return "温度計一覧"
	elif url_name == 'create_thermometer': return "温度計登録"
	elif url_name == 'detail_thermometer':
		thermometer = get_object_or_404(models.Thermometer, pk=kwargs['pk'])
		return "温度計詳細:" + thermometer.name
	elif url_name == 'delete_thermometer':
		thermometer = get_object_or_404(models.Thermometer, pk=kwargs['pk'])
		return "温度計情報削除:" + thermometer.name
	elif url_name == 'update_thermometer':
		thermometer = get_object_or_404(models.Thermometer, pk=kwargs['pk'])
		return "温度計情報更新:" + thermometer.name
	#フロア関連
	elif url_name == 'create_floor':
		return "フロア登録:{}F".format(kwargs['floor'])
	elif url_name == 'detail_floor':
		floor = get_object_or_404(models.Floor, pk=kwargs['pk'])
		return "フロア詳細:{}F".format(floor.floor)
	elif url_name == 'delete_floor':
		floor = get_object_or_404(models.Floor, pk=kwargs['pk'])
		return "フロア情報削除:{}F".format(floor.floor)
	elif url_name == 'update_floor':
		floor = get_object_or_404(models.Floor, pk=kwargs['pk'])
		return "フロア情報更新:{}F".format(floor.floor)

	return url_name


def get_breadcrumb(url_name, kwargs=None, no_url=False):
	breadcrumb = {'title': get_title(url_name, kwargs=kwargs)}
	if no_url: pass
	else:
		if kwargs is None:
			breadcrumb['url'] = reverse_lazy('watch_temp:'+url_name)
		else:
			breadcrumb['url'] = reverse('watch_temp:'+url_name, kwargs=kwargs)
	return breadcrumb
