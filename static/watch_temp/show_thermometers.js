function setThermometersPos(floor, thermometersParent){
	const ts = thermometersParent.getElementsByClassName('thermometer');

	if(ts == null || ts.length == 0) return;

	const pRect = thermometersParent.getBoundingClientRect();
	const fRect = floor.getBoundingClientRect();
	const tRect = ts[0].getBoundingClientRect();
	const dx = fRect.left - pRect.left - tRect.width  / 2;
	const dy = fRect.top  - pRect.top  - tRect.height / 2;

	for(var t of ts){
		t.style.left = String(Number(t.dataset.posX) * fRect.width  + dx) + 'px';
		t.style.top  = String(Number(t.dataset.posY) * fRect.height + dy) + 'px';
	}
}
