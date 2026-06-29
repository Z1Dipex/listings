@login_required
def profile(request):
    user_report = DataSet.objects.filter(user=request.user).first()
    
    if not user_report:
        user_report = DataSet.objects.create(user=request.user)

    if request.method == 'POST':
        if 'generate_title' in request.POST:
            return generate_title_document(request, user_report)
        if 'generate_diary' in request.POST:
            return generate_diary_document(request, user_report)
        if 'generate_task' in request.POST:
            return generate_task_document(request, user_report)

        if request.POST.get('familia'):
            user_report.familia = request.POST['familia']
        if request.POST.get('name'):
            user_report.name = request.POST['name']
        if request.POST.get('otchestvo'):
            user_report.otchestvo = request.POST['otchestvo']
        if request.POST.get('tip'):
            try:
                user_report.prac_type = PracType.objects.get(type_name=request.POST['tip'])
            except PracType.DoesNotExist:
                pass
        if request.POST.get('module'):
            user_report.module = request.POST['module']
        if request.POST.get('specialization'):
            user_report.specialization = request.POST['specialization']
        if request.POST.get('kurs'):
            user_report.kurs = request.POST['kurs']
        if request.POST.get('group'):
            user_report.group = request.POST['group']
        if request.POST.get('hours'):
            try:
                user_report.hours = int(request.POST['hours'])
            except ValueError:
                user_report.hours = None
        if request.POST.get('mdk1'):
            user_report.mdk1 = request.POST['mdk1']
        if request.POST.get('mdk2'):
            user_report.mdk2 = request.POST['mdk2']
        if request.POST.get('mdk3'):
            user_report.mdk3 = request.POST['mdk3']
        if request.POST.get('mdk4'):
            user_report.mdk4 = request.POST['mdk4']
        if request.POST.get('begin_date'):
            date_parts = request.POST['begin_date'].split('-')
            if len(date_parts) == 3:
                user_report.date_begin = f"{date_parts[2]}.{date_parts[1]}.{date_parts[0]}"
        if request.POST.get('finish_date'):
            date_parts = request.POST['finish_date'].split('-')
            if len(date_parts) == 3:
                user_report.date_finish = f"{date_parts[2]}.{date_parts[1]}.{date_parts[0]}"
        if request.POST.get('head1'):
            user_report.head1 = request.POST['head1']
        if request.POST.get('head2'):
            user_report.head2 = request.POST['head2']
        if request.POST.get('ruc_pract'):
            user_report.ruc_pract = request.POST['ruc_pract']
        if request.POST.get('year'):
            try:
                user_report.year = int(request.POST['year'])
            except ValueError:
                user_report.year = None
        
        user_report.save()
        messages.success(request, 'Данные успешно сохранены!')
        return redirect('/profile/')
    
    # Обработка GET запроса (показываем форму)
    begin_date_for_input = ''
    finish_date_for_input = ''
    
    if user_report.date_begin:
        try:
            date_parts = user_report.date_begin.split('.')
            if len(date_parts) == 3:
                begin_date_for_input = f"{date_parts[2]}-{date_parts[1]}-{date_parts[0]}"
        except:
            pass
    
    if user_report.date_finish:
        try:
            date_parts = user_report.date_finish.split('.')
            if len(date_parts) == 3:
                finish_date_for_input = f"{date_parts[2]}-{date_parts[1]}-{date_parts[0]}"
        except:
            pass
    
    prac_types = PracType.objects.all()
    
    # Проверяем наличие шаблонов
    has_title_template = DocTemplate.objects.filter(template_type='title', is_active=True).exists()
    has_diary_template = DocTemplate.objects.filter(template_type='diary', is_active=True).exists()
    has_task_template = DocTemplate.objects.filter(template_type='task', is_active=True).exists()
    
    return render(request, "profile.html", {
        "user_report": user_report,
        "prac_types": prac_types,
        "begin_date_for_input": begin_date_for_input,
        "finish_date_for_input": finish_date_for_input,
        "has_title_template": has_title_template,
        "has_diary_template": has_diary_template,
        "has_task_template": has_task_template,
    })
