from django.shortcuts import redirect, render, get_object_or_404
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


class SetThermometerPos(mixins.MyLoginRequiredMixin, TemplateView):
	template_name = "watch_temp/set_thermometer_pos.html"
	def post(self, request, *args, **kwargs):
		floor = get_object_or_404(models.Floor, id=kwargs['floor_id'])

		ls = {} # {シリアル番号 : {'using': 使用中か, 'pos_x': x座標, 'pos_y': y座標}}
		for key in request.POST:
			ss = key.split('_')
			if len(ss) == 2:
				if not ss[0] in ls: #if serial is not in 
					ls[ss[0]] = {'using': False, 'posx': 0, 'posy': 0}
				if ss[1] == 'using':
					ls[ss[0]]['using'] = bool(request.POST[key])
				if ss[1] == 'posx':
					ls[ss[0]]['posx'] = float(request.POST[key])
				if ss[1] == 'posy':
					ls[ss[0]]['posy'] = float(request.POST[key])
		for serial in ls:
			try:
				t = models.Thermometer.objects.get(serial=serial)
			except: pass
			else:
				if ls[serial]['using']:
					t.floor = floor
					t.pos_x = ls[serial]['posx']
					t.pos_y = ls[serial]['posy']
					t.save()
				else:
					t.floor = None
					t.save()
		return redirect('watch_temp:index')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		floor = get_object_or_404(models.Floor, id=kwargs['floor_id'])
		context['floor'] = floor
		#どこにも配置されていない温度計(の名前、使用中か)をcontextに追加
		thermometers = models.Thermometer.objects.filter(floor=None)
		ts = []
		for t in thermometers:
			ts.append({'serial': t.serial, 'name': t.name, 'using': False})
		#当該フロアに配置されている温度計(の名前、使用中か、位置)をcontextに追加
		thermometers = models.Thermometer.objects.filter(floor=floor)
		for t in thermometers:
			ts.append({'serial': t.serial, 'name': t.name, 'using': True, 'posx': t.pos_x, 'posy': t.pos_y})
		context['thermometers'] = ts
		return context


class CreateThermometer(mixins.MyLoginRequiredMixin, CreateView):
	template_name = "watch_temp/create_thermometer.html"
	model = models.Thermometer
	fields = ['name', 'serial', 'comment']
	def get_success_url(self):
		return reverse("watch_temp:detail_thermometer", kwargs={'pk': self.object.id})


class DetailBuilding(mixins.MyLoginRequiredMixin, DetailView):
	template_name = "watch_temp/detail_building.html"
	model = models.Building

	def get_context_data(self, **kwargs):
		context = super().get_context_data()
		building = context['building']
		fs = [{'floor': i+1, 'id': None} for i in range(building.floor_count)]
		floors = models.Floor.objects.filter(building=building)
		for floor in floors:
			try:
				fs[floor.floor - 1]['id'] = floor.id
			except IndexError: pass
		fs.reverse()
		context['floors'] = fs
		return context


class DetailFloor(mixins.MyLoginRequiredMixin, DetailView):
	template_name = "watch_temp/detail_floor.html"
	model = models.Floor


class DetailThermometer(mixins.MyLoginRequiredMixin, DetailView):
	template_name = "watch_temp/detail_thermometer.html"
	model = models.Thermometer
