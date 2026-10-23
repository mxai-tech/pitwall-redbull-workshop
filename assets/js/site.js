'use strict';
(() => {
  const $ = (id) => document.getElementById(id);
  const toc = $('page-toc');
  document.querySelectorAll('.content h2').forEach((heading, index) => {
    if (!heading.id) heading.id = `tema-${index + 1}`;
    const link = document.createElement('a');
    link.href = `#${heading.id}`;
    link.textContent = heading.textContent;
    toc?.append(link);
  });
  function download(name, text, type = 'text/plain;charset=utf-8') {
    const url = URL.createObjectURL(new Blob([text], { type }));
    const link = document.createElement('a');
    link.href = url;
    link.download = name;
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  if ($('personality-tool')) {
    const ids = ['engineer', 'driver', 'number', 'style', 'risk', 'relation', 'golden', 'radio'];
    const value = (id) => $(id).value.trim();
    // JSON quoted strings are valid YAML scalars, including embedded quotes and newlines.
    const quote = (s) => JSON.stringify(s);
    function profile() {
      const values = { ingeniero: value('engineer'), piloto: value('driver'), numero: Number(value('number')), estilo: value('style'), riesgo: Number(value('risk')), reserva_boost: 40, relacion: value('relation'), regla_de_oro: value('golden'), frase_radio: value('radio'), descripcion_avatar: 'Piloto ficticio, sin logotipos ni rostros reales' };
      return Object.entries(values).map(([k, v]) => `${k}: ${typeof v === 'number' ? v : quote(v)}`).join('\n') + '\n';
    }
    function validate() {
      const number = Number(value('number'));
      if (!Number.isInteger(number) || number < 1 || number > 99 || [3, 6].includes(number)) return 'Elige un número de 1 a 99, excepto 3 y 6.';
      if (['engineer', 'driver', 'golden', 'radio'].some((id) => !value(id))) return 'Completa los nombres, la regla de oro y la frase de radio.';
      return '';
    }
    function updateProfile() {
      $('risk-value').textContent = `${value('risk')} / 5`;
      $('profile-preview').textContent = profile();
      $('profile-error').textContent = validate();
      $('profile-summary').textContent = `Perfil ${value('style')}, riesgo ${value('risk')}/5; relación con Estrategia: ${value('relation')}. Es una instrucción para el modelo, no una garantía de comportamiento.`;
    }
    ids.forEach((id) => $(id).addEventListener('input', updateProfile));
    $('download-profile').addEventListener('click', () => {
      updateProfile();
      if (validate()) { $('number').focus(); return; }
      download('ficha.yaml', profile(), 'text/yaml;charset=utf-8');
    });
    updateProfile();
  }
  if ($('energy-lab')) {
    const ids = ['threshold', 'rival-gap', 'battery', 'distance', 'has-rival', 'require-rival'];
    let tested = false;
    function code() {
      const rival = $('require-rival').checked;
      return `def elegir_energia(bateria, gap_adelante):\n    umbral_boost = ${$('threshold').value}\n${rival ? `    rival_cerca = (\n        gap_adelante is not None\n        and gap_adelante < ${Number($('rival-gap').value).toFixed(1)}\n    )\n` : ''}\n    if bateria >= umbral_boost${rival ? ' and rival_cerca' : ''}:\n        return "BOOST"\n\n    return "EQUILIBRIO"\n`;
    }
    function update() {
      $('threshold-value').textContent = `${$('threshold').value} %`;
      $('gap-value').textContent = `${Number($('rival-gap').value).toFixed(1)} s`;
      $('energy-code').textContent = code();
      $('distance').disabled = !$('has-rival').checked;
      $('rival-gap').disabled = !$('require-rival').checked;
      if (tested) {
        $('energy-result').classList.add('stale');
        $('energy-result').replaceChildren();
        const p = document.createElement('p');
        p.textContent = 'Cambiaste las condiciones. Pulsa “Probar decisión” para actualizar el resultado.';
        $('energy-result').append(p);
      }
    }
    ids.forEach((id) => $(id).addEventListener('input', update));
    $('test-energy').addEventListener('click', () => {
      const battery = Number($('battery').value);
      const distance = Number($('distance').value);
      const threshold = Number($('threshold').value);
      const gap = Number($('rival-gap').value);
      const required = $('require-rival').checked;
      const hasRival = $('has-rival').checked;
      const result = $('energy-result');
      result.classList.remove('stale');
      result.replaceChildren();
      tested = true;
      const invalidBattery = $('battery').value === '' || !Number.isFinite(battery) || battery < 0 || battery > 100;
      const invalidDistance = hasRival && ($('distance').value === '' || !Number.isFinite(distance) || distance < 0);
      if (invalidBattery || invalidDistance) {
        result.textContent = 'Introduce una batería de 0 a 100 y una distancia válida, igual o mayor que cero.';
        return;
      }
      const enough = battery >= threshold;
      const nearby = hasRival && distance < gap;
      const boost = enough && (!required || nearby);
      const strong = document.createElement('strong');
      strong.textContent = boost ? 'BOOST' : 'EQUILIBRIO';
      const explanation = document.createElement('p');
      explanation.textContent = `Batería: ${battery} % ${enough ? '≥' : '<'} ${threshold} %. ${required ? (hasRival ? `Rival a ${distance.toFixed(1)} s; ${nearby ? 'cumple' : 'no cumple'} distancia < ${gap.toFixed(1)} s.` : 'No hay rival adelante: la condición no se cumple.') : 'No se exige un rival cercano.'} Esta prueba evalúa la condición inicial; no simula seis vueltas.`;
      result.append(strong, explanation);
    });
    $('download-energy').addEventListener('click', () => download('regla_energia.py', '# Fragmento didáctico; no es un Director completo.\n' + code()));
    $('reset-energy').addEventListener('click', () => {
      $('threshold').value = 40;
      $('rival-gap').value = 1;
      $('battery').value = 50;
      $('distance').value = 0.8;
      $('has-rival').checked = true;
      $('require-rival').checked = true;
      tested = false;
      update();
      $('energy-result').classList.remove('stale');
      $('energy-result').textContent = 'Prepara tu primera prueba y pulsa “Probar decisión”.';
    });
    update();
  }
})();
