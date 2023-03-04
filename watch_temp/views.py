from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from . import models, mixins, forms

class Index(mixins.MyLoginRequiredMixin, TemplateView):
	template_name = "watch_temp/index.html"


class AboutOriginalSystem(mixins.MyLoginRequiredMixin, TemplateView):
	template_name = "watch_temp/about_original_system.html"


class CreateBuilding(mixins.MyLoginRequiredMixin, CreateView):
	template_name = "watch_temp/create_building.html"
	model = models.Building
	fields = ['name', 'floor_count', 'comment']
	def get_success_url(self):
		return reverse("watch_temp:detail_building", kwargs={"pk": self.object.id})


class CreateFloor(mixins.MyLoginRequiredMixin, CreateView):
	template_name = "watch_temp/create_floor.html"
	model = models.Floor
	fields = ['name', 'comment', 'image']
	def check_building_id_and_floor(self, building_id, floor):
		err_msgs = ["新規フロア情報の登録に失敗しました。"]
		try:
			building = models.Building.objects.get(id=building_id)
		except:
			err_msgs.append("URLのcreate_floorの直後の数字は建物の識別番号です。<br>しかし、入力された"+str(project_id)+"には対応する建物がありません。")
			return err_msgs

		if floor < 1 or floor > building.floor_count:
			err_msgs.append("URLのcreate_floorの1つ後の数字は建物の識別番号、2つ後の数字はフロアの階数です。<br>"+str(building_id)+"に対応する建物は"+str(building.floor_count)+"階建てです。したがって入力された"+str(floor)+"は存在しない階です。")
			return err_msgs
		try:
			f = models.Floor.objects.get(building=building, floor=floor)
		except: pass
		else:
			err_msgs.append("URLのcreate_floorの1つ後の数字は建物の識別番号、2つ後の数字はフロアの階数です。<br>入力された、/"+str(building_id)+"/"+str(floor)+"に対応するデータは既に登録されています。")
			return err_msgs
		return None

	def get(self, request, **kwargs):
		err_msgs = self.check_building_id_and_floor(kwargs["building_id"], self.kwargs["floor"])
		if not err_msgs is None:
			return render(request, "watch_temp/error.html", {"error_messages": err_msgs})
		else:
			return super().get(request, **kwargs)

	def post(self, request, **kwargs):
		err_msgs = self.check_building_id_and_floor(kwargs["building_id"], self.kwargs["floor"])
		if not err_msgs is None:
			return render(request, "watch_temp/error.html", {"error_messages": err_msgs})
		else:
			return super().post(request, **kwargs)

	def form_valid(self, form):
		form.instance.building_id = self.kwargs["building_id"]
		form.instance.floor = self.kwargs["floor"]
		return super().form_valid(form)

	def get_success_url(self):
		return reverse("watch_temp:detail_floor", kwargs={"pk": self.object.id})


class DetailBuilding(mixins.MyLoginRequiredMixin, DetailView):
	template_name = "watch_temp/detail_building.html"
	model = models.Building


class DetailFloor(mixins.MyLoginRequiredMixin, DetailView):
	template_name = "watch_temp/detail_floor.html"
	model = models.Floor
