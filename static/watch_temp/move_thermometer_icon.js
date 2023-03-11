function initThermometers(thermometersParent){
	const ts = document.getElementsByClassName('thermometer');
	if(ts == null || ts.length == 0){
		thermometersParent.style.height = '0px';
		return;
	}
	const pRect = thermometersParent.getBoundingClientRect();
	const tRect = ts[0].getBoundingClientRect();

	const c = Math.floor(pRect.width / tRect.width);
	const r = Math.ceil(ts.length / c);
	thermometersParent.style.height = String(tRect.height * r) + 'px';
	const sx = (pRect.width - c * tRect.width) / 2;
	for(var i=0; i<ts.length; ++i){
		var ic = i % c;
		var ir = Math.floor(i / c);
		ts[i].dataset.initLeft = String(ic * tRect.width  + sx) + 'px';
		ts[i].dataset.initTop  = String(ir * tRect.height) + 'px';
		ts[i].style.left = ts[i].dataset.initLeft;
		ts[i].style.top  = ts[i].dataset.initTop;
	}
}


function startMoveThermometers(floor, thermometersParent){
	const ts = document.getElementsByClassName('thermometer');

	for(const t of ts){
		t.onmousedown = function(){
			var startRect = t.getBoundingClientRect();
			var startX = startRect.left - event.clientX - scrollX;
			var startY = startRect.top  - event.clientY - scrollY;

			window.onmousemove = function(){
				if (window.getSelection)
					window.getSelection().removeAllRanges();

				var pRect = thermometersParent.getBoundingClientRect();
				t.style.left = String(startX + event.clientX + scrollX - pRect.left) + 'px';
				t.style.top  = String(startY + event.clientY + scrollY - pRect.top)  + 'px';
			};

			window.onmouseup = function(){
				var inputUsing = document.getElementsByName(t.dataset.serial + '_using')[0];

				var endRect = t.getBoundingClientRect();
				var fRect = floor.getBoundingClientRect();
				var x = (endRect.left + endRect.right)  / 2;
				var y = (endRect.top  + endRect.bottom) / 2;

				if(x >= fRect.left && x <= fRect.right && y >= fRect.top && y <= fRect.bottom){
					inputUsing.value = 'True';
					var inputPosX = document.getElementsByName(t.dataset.serial + '_posx')[0];
					var inputPosY = document.getElementsByName(t.dataset.serial + '_posy')[0];
					inputPosX.value = String(( x - fRect.left)   / fRect.width);
					inputPosY.value = String((-y + fRect.bottom) / fRect.height);
				}
				else{
					inputUsing.value = 'False';

					t.style.left = t.dataset.initLeft;
					t.style.top  = t.dataset.initTop;
				}

				window.onmousemove = null;
				window.onmouseup = null;
			};
		};
	}
}
