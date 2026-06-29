def decline_fio_genitive(familia, name, otchestvo):
    def decline_familia(f):
        if not f:
            return ''
        # Женские фамилии на -а, -я
        if f.endswith('а'):
            return f[:-1] + 'ой'
        if f.endswith('я'):
            return f[:-1] + 'ой'
        if f.endswith('ва'):
            return f[:-2] + 'вой'
        if f.endswith('на'):
            return f[:-2] + 'ной'
        # Мужские фамилии
        if f.endswith('ий'):
            return f[:-2] + 'его'
        if f.endswith('ый'):
            return f[:-2] + 'ого'
        if f.endswith('ой'):
            return f[:-2] + 'ого'
        if f.endswith('ь'):
            return f[:-1] + 'я'
        if f[-1] in 'бвгджзйклмнпрстфхцчшщ':
            return f + 'а'
        return f
    
    def decline_name(n):
        if not n:
            return ''
        if n.endswith('а'):
            return n[:-1] + 'ы'
        if n.endswith('я'):
            return n[:-1] + 'и'
        if n.endswith('й'):
            return n[:-1] + 'я'
        if n.endswith('ь'):
            return n[:-1] + 'я'
        if n[-1] in 'бвгджзйклмнпрстфхцчшщ':
            return n + 'а'
        return n
    
    def decline_otchestvo(o):
        if not o:
            return ''
        if o.endswith('на'):
            return o[:-2] + 'ны'
        if o.endswith('вна'):
            return o[:-3] + 'вны'
        if o.endswith('чна'):
            return o[:-3] + 'чны'
        if o.endswith('ч'):
            return o + 'а'
        if o.endswith('й'):
            return o[:-1] + 'я'
        if o.endswith('а'):
            return o[:-1] + 'ы'
        return o + 'а'
    
    fam = decline_familia(familia)
    nam = decline_name(name)
    otch = decline_otchestvo(otchestvo)
    
    result_parts = []
    if fam:
        result_parts.append(fam)
    if nam:
        result_parts.append(nam)
    if otch:
        result_parts.append(otch)
    
    return ' '.join(result_parts)


def decline_fio_dative(familia, name, otchestvo):
    def decline_familia_dative(f):
        if not f:
            return ''
        if f.endswith('а'):
            return f[:-1] + 'ой'
        if f.endswith('я'):
            return f[:-1] + 'ой'
        if f.endswith('ва'):
            return f[:-2] + 'вой'
        if f.endswith('на'):
            return f[:-2] + 'ной'
        if f.endswith('ий'):
            return f[:-2] + 'ему'
        if f.endswith('ый'):
            return f[:-2] + 'ому'
        if f.endswith('ой'):
            return f[:-2] + 'ому'
        if f.endswith('ь'):
            return f[:-1] + 'ю'
        if f[-1] in 'бвгджзйклмнпрстфхцчшщ':
            return f + 'у'
        return f
    
    def decline_name_dative(n):
        if not n:
            return ''
        if n.endswith('а'):
            return n[:-1] + 'е'
        if n.endswith('я'):
            return n[:-1] + 'е'
        if n.endswith('й'):
            return n[:-1] + 'ю'
        if n.endswith('ь'):
            return n[:-1] + 'ю'
        if n[-1] in 'бвгджзйклмнпрстфхцчшщ':
            return n + 'у'
        return n
    
    def decline_otchestvo_dative(o):
        if not o:
            return ''
        if o.endswith('на'):
            return o[:-2] + 'не'
        if o.endswith('вна'):
            return o[:-3] + 'вне'
        if o.endswith('чна'):
            return o[:-3] + 'чне'
        if o.endswith('ч'):
            return o + 'у'
        if o.endswith('й'):
            return o[:-1] + 'ю'
        if o.endswith('а'):
            return o[:-1] + 'е'
        return o + 'у'
    
    fam = decline_familia_dative(familia)
    nam = decline_name_dative(name)
    otch = decline_otchestvo_dative(otchestvo)
    
    result_parts = []
    if fam:
        result_parts.append(fam)
    if nam:
        result_parts.append(nam)
    if otch:
        result_parts.append(otch)
    
    return ' '.join(result_parts)


def format_date_for_title(date_str):
    """
    Форматирует дату для титульного листа: '2' декабря 2025
    Вход: 02.12.2025
    Выход: "2" декабря 2025
    """
    if not date_str:
        return ''
    
    try:
        parts = date_str.split('.')
        if len(parts) != 3:
            return date_str
        
        day = str(int(parts[0]))
        month_num = parts[1]
        year = parts[2]
        
        months = {
            '01': 'января', '02': 'февраля', '03': 'марта', '04': 'апреля',
            '05': 'мая', '06': 'июня', '07': 'июля', '08': 'августа',
            '09': 'сентября', '10': 'октября', '11': 'ноября', '12': 'декабря'
        }
        
        month_name = months.get(month_num, month_num)
        
        return f'"{day}" {month_name} {year}'
    
    except Exception:
        return date_str


def normalize_prac_type_for_title(prac_type):
    """
    Приводит тип практики к формату для заголовка
    Производственная → ПРОИЗВОДСТВЕННОЙ
    Учебная → УЧЕБНОЙ
    """
    if not prac_type:
        return "ПРОИЗВОДСТВЕННОЙ"
    
    if prac_type.lower() == "производственная":
        return "ПРОИЗВОДСТВЕННОЙ"
    elif prac_type.lower() == "учебная":
        return "УЧЕБНОЙ"
    else:
        return prac_type.upper()


def to_genitive_simple(full_name):
    def transform_last_name(name):
        if name.endswith('ко'): 
            return name
        if name.endswith('ий'): 
            return name[:-2] + 'ия'
        if name.endswith('а'):  
            return name[:-1] + 'ой'
        if name.endswith('я'): 
            return name[:-1] + 'ой'
        return name + 'а'
    
    def transform_first_name(name):
        exceptions = {'дмитрий': 'дмитрия', 'илья': 'ильи'}
        if name.lower() in exceptions:
            return exceptions[name.lower()].capitalize()
        if name.endswith('а'): 
            return name[:-1] + 'ы'
        if name.endswith('я'): 
            return name[:-1] + 'и'
        if name.endswith('ий'):
            return name[:-2] + 'ия'
        return name + 'а'
    
    def transform_otchestvo(o):
        if not o:
            return ''
        if o.endswith('на'):
            return o[:-2] + 'ны'
        if o.endswith('вна'):
            return o[:-3] + 'вны'
        if o.endswith('чна'):
            return o[:-3] + 'чны'
        if o.endswith('а'):
            return o[:-1] + 'ы'
        return o + 'а'
    
    parts = full_name.split()
    if not parts:
        return ''
    
    result = [transform_last_name(parts[0])]
    if len(parts) >= 2:
        result.append(transform_first_name(parts[1]))
    if len(parts) >= 3:
        result.append(transform_otchestvo(parts[2]))
    return " ".join(result)
