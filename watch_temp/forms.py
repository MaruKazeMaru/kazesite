from django import forms

class CreateFloorForm(forms.Form):
	name = forms.CharField(label="name:")
	set_new_image = forms.BooleanField(label="set new image:")
	image_id = forms.IntegerField(label="image id:", min_value=1, localize=False, required=False)
	new_image = forms.ImageField(label="new image:", required=False)
	comment = forms.CharField(label="comment:")
