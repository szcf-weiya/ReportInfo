for i in xrange(len(news)):
    if i == 98:
        print(news[i])
    try:
        # 合并<span>
        
        # 去除<span>num</span>
        inews = str(news[i])
        correct = span_rm.findall(inews)
        if not correct:
            pass
        else:    
            print(inews)
            for i in xrange(len(correct)):
                span_rm_tmp = re.compile('<span>'+correct[i]+'</span>')
                inews = span_rm_tmp.sub(correct[i], inews)
        info = date_pattern.findall(inews.decode('utf8'))
        if i == 3:    
            print(info)
        if len(info) >= 1:
            datelist.append(info[0])
    except:
        continue