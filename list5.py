# views.py — Генерация документов (титульный лист, дневник, задание)

@login_required
def generate_title_document(request, user_report):
    """
    Генерация титульного листа отчета по практике
    """
    temp_file_path = None
    try:
        template = DocTemplate.objects.get(template_type='title', is_active=True)

        if user_report.prac_type and user_report.prac_type.type_name == 'Учебная':
            practice_type = "УЧЕБНОЙ"
        else:
            practice_type = "ПРОИЗВОДСТВЕННОЙ"

        # Родительный падеж (кого?) - Кульковой Ульяны Андреевны
        fio_genitive = decline_fio_genitive(
            user_report.familia or '',
            user_report.name or '',
            user_report.otchestvo or ''
        )

        date_begin_formatted = format_date_for_title(user_report.date_begin or '')
        date_finish_formatted = format_date_for_title(user_report.date_finish or '')

        def underline_if_empty(value, length=8):
            if not value or value.strip() == '':
                return '_' * length
            return value

        context = {
            'tip': practice_type,
            'fio': fio_genitive,
            'module': underline_if_empty(user_report.module, 8),
            'specialization': underline_if_empty(user_report.specialization, 8),
            'kurs': user_report.kurs or '',
            'group': user_report.group or '',
            'date_begin': date_begin_formatted,
            'date_finish': date_finish_formatted,
            'head1': underline_if_empty(user_report.head1, 8),
            'head2': underline_if_empty(user_report.head2, 8),
            'ruc_pract': underline_if_empty(user_report.ruc_pract, 8),
            'year': user_report.year or datetime.now().year,
        }

        doc = DocxTemplate(template.file.path)
        doc.render(context)

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.docx')
        temp_file_path = temp_file.name
        temp_file.close()

        doc.save(temp_file_path)
        time.sleep(0.1)

        with open(temp_file_path, 'rb') as f:
            file_content = f.read()

        try:
            os.remove(temp_file_path)
        except:
            pass

        filename = f"{user_report.familia}_{user_report.name}_Титульный_лист_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"

        response = HttpResponse(file_content, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        messages.success(request, 'Титульный лист успешно сгенерирован!')
        return response

    except DocTemplate.DoesNotExist:
        messages.error(request, 'Шаблон титульного листа не найден')
    except Exception as e:
        messages.error(request, f'Ошибка: {str(e)}')
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except:
                pass

    return redirect('/profile/')


@login_required
def generate_diary_document(request, user_report):
    """
    Генерация дневника практики
    """
    temp_file_path = None
    try:
        template = DocTemplate.objects.get(template_type='diary', is_active=True)

        if user_report.prac_type and user_report.prac_type.type_name == 'Учебная':
            practice_type = "УЧЕБНОЙ"
        else:
            practice_type = "ПРОИЗВОДСТВЕННОЙ"

        # Сокращаем модуль до ПМ.12
        module_full = user_report.module or ''
        module_short = module_full
        if module_full.startswith('ПМ'):
            import re
            match = re.match(r'(ПМ\.?\s*\d+)', module_full, re.IGNORECASE)
            if match:
                module_short = match.group(1).replace(' ', '')
            else:
                module_short = module_full[:8] if len(module_full) > 8 else module_full
        else:
            module_short = module_full[:8] if len(module_full) > 8 else module_full

        context = {
            'tip': practice_type,
            'familia': user_report.familia or '',
            'name': user_report.name or '',
            'otchestvo': user_report.otchestvo or '',
            'kurs': user_report.kurs or '',
            'group': user_report.group or '',
            'specialization': user_report.specialization or '',
            'head1': user_report.head1 or '',
            'head2': user_report.head2 or '',
            'ruc_pract': user_report.ruc_pract or '',
            'module': module_short,
        }

        doc = DocxTemplate(template.file.path)
        doc.render(context)

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.docx')
        temp_file_path = temp_file.name
        temp_file.close()

        doc.save(temp_file_path)
        time.sleep(0.1)

        with open(temp_file_path, 'rb') as f:
            file_content = f.read()

        try:
            os.remove(temp_file_path)
        except:
            pass

        filename = f"{user_report.familia}_{user_report.name}_Дневник_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"

        response = HttpResponse(file_content, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        messages.success(request, 'Дневник успешно сгенерирован!')
        return response

    except DocTemplate.DoesNotExist:
        messages.error(request, 'Шаблон дневника не найден')
    except Exception as e:
        messages.error(request, f'Ошибка: {str(e)}')
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except:
                pass

    return redirect('/profile/')


@login_required
def generate_task_document(request, user_report):
    """
    Генерация задания на практику
    """
    temp_file_path = None
    try:
        template = DocTemplate.objects.get(template_type='task', is_active=True)

        # Первый тип практики (в фразе "на учебную практическую подготовку")
        if user_report.prac_type and user_report.prac_type.type_name == 'Учебная':
            practice_type_first = "учебную"
        else:
            practice_type_first = "производственную"
        
        # Второй тип практики (в тексте "в период учебной практической подготовки")
        if user_report.prac_type and user_report.prac_type.type_name == 'Учебная':
            practice_type_second = "учебной"
        else:
            practice_type_second = "производственной"

        # Дательный падеж (кому?) - Кульковой Ульяне Андреевне
        fio_dative = decline_fio_dative(
            user_report.familia or '',
            user_report.name or '',
            user_report.otchestvo or ''
        )

        context = {
            'tip': practice_type_first,      # учебную или производственную
            'tip2': practice_type_second,    # учебной или производственной
            'fio_dative': fio_dative,        # Кульковой Ульяне Андреевне
            'familia': user_report.familia or '',
            'name': user_report.name or '',
            'otchestvo': user_report.otchestvo or '',
            'specialization': user_report.specialization or '',
            'module': user_report.module or '',
            'mdk1': user_report.mdk1 or '',
            'mdk2': user_report.mdk2 or '',
            'mdk3': user_report.mdk3 or '',
            'mdk4': user_report.mdk4 or '',
            'hours': user_report.hours or '',
            'date_begin': user_report.date_begin or '',
            'date_finish': user_report.date_finish or '',
            'head1': user_report.head1 or '',
            'year': user_report.year or datetime.now().year,
        }

        doc = DocxTemplate(template.file.path)
        doc.render(context)

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.docx')
        temp_file_path = temp_file.name
        temp_file.close()

        doc.save(temp_file_path)
        time.sleep(0.1)

        with open(temp_file_path, 'rb') as f:
            file_content = f.read()

        try:
            os.remove(temp_file_path)
        except:
            pass

        filename = f"{user_report.familia}_{user_report.name}_Задание_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"

        response = HttpResponse(file_content, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        messages.success(request, 'Задание успешно сгенерировано!')
        return response

    except DocTemplate.DoesNotExist:
        messages.error(request, 'Шаблон задания не найден')
    except Exception as e:
        messages.error(request, f'Ошибка: {str(e)}')
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except:
                pass

    return redirect('/profile/')
