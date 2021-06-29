        document.getElementsByName('kinput_name')[0].addEventListener("keydown", log);
        document.getElementsByName('kinput_name_2')[0].addEventListener("keydown", log_2);
        document.getElementsByClassName('')
        const list_producers = [];
        const list_actors = [];
        let datas;
        const title = document.getElementsByName('Title')
        let imgs = document.createElement('img');
        let form_imgs = document.createElement('input');
        const droparea = document.getElementsByClassName('drop-area')[0];
        const replacer_as = document.getElementsByClassName('replacer_as')[0]

        function open_files() {
            const input = document.createElement('input');
            input.addEventListener('change', function () {
                image_update(input.files[0])
            })
            input.type = 'file';
            input.click();
        }

        function drop(event) {
            event.preventDefault();
            const data = event.dataTransfer.files[0];
            image_update(data);
            return false
        }

        function image_update(data_func) {
            let reader = new FileReader();
            if (data_func.type === 'image/png' || data_func.type === 'image/jpeg') {
                reader.readAsDataURL(data_func);
                reader.onloadend = function () {
                    replacer_as.innerHTML = 'If you need to replace it, put it again';
                    imgs.src = String(reader.result);
                    imgs.className = 'img_ava';
                    if (datas !== undefined) {
                        droparea.removeChild(datas);
                    }
                    droparea.appendChild(imgs);
                    form_imgs.value = imgs.src;
                    form_imgs.name = 'imgs_back';
                    form_imgs.style.display = 'none';
                    droparea.appendChild(form_imgs);
                    datas = imgs;
                }
            } else {
                replacer_as.innerHTML = 'Only PNG or JPG can be put to me!';
            }
        }

        function dragleavel(event) {
            event.preventDefault();
            droparea.style.borderColor = "#CCC";
        }

        function dragoverl(event) {
            event.preventDefault();
            droparea.style.borderColor = "#957DAD";
        }

        function log_2(e) {
            if (e.key === ',') {
                e.preventDefault();
                handler_off_add('kinput_name_2', log_2, 4)
            }
            if (e.key === 'Backspace') {
                handler_off_backspace('kinput_name_2', e)
            }
        }

        function log(e) {
            if (e.key === ',') {
                e.preventDefault();
                handler_off_add('kinput_name', log, 0)
            }
            if (e.key === 'Backspace') {
                handler_off_backspace('kinput_name', e)
            }
        }

        function handler_off_backspace(element_name, e) {
            const text = document.getElementsByName(element_name);
            if (text[text.length - 1].value === '') {
                const count = text.length;
                if (count > 1) {
                    text[text.length - 1].remove();
                    text[text.length - 1].removeAttribute('readonly');
                    text[text.length - 1].style.pointerEvents = 'auto';
                    text[text.length - 1].focus();
                    e.preventDefault();
                    if (element_name === 'kinput_name') {
                        list_producers.pop();
                    } else {
                        list_actors.pop();
                    }
                }
            }
        }

        function handler_off_add(element_name, element_number, x_minus) {
            const x = document.getElementById("form");
            const new_field = document.createElement("input");
            new_field.type = 'text';
            new_field.name = element_name;
            new_field.value = '';
            const pos = x.childElementCount;
            x.insertBefore(new_field, x.childNodes[pos - x_minus]);
            const new_element = document.getElementsByName(element_name);
            new_element[new_element.length - 1].addEventListener("keydown", element_number)
            new_element[new_element.length - 1].focus()
            new_element[new_element.length - 2].setAttribute('readonly', 'readonly')
            new_element[new_element.length - 2].style.pointerEvents = 'none';
            if (element_name === 'kinput_name') {
                list_producers.push({'producer': String(new_element[new_element.length - 2].value)})
            } else {
                list_actors.push({'actor': String(new_element[new_element.length - 2].value)})
            }
        }