from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.contrib import messages
from django.db.models import Max, Sum
from xhtml2pdf import pisa
import pandas as pd
from .forms import Achatforms, Articlesforms, Venteforms, Clientforms
from .models import AchatModel, AriclesModel, Bilan, VenteModel, ClientModel

# Export data to Excel functions
def export_clients_to_excel(request):
    clients = ClientModel.objects.all().values()
    df = pd.DataFrame(clients)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=clients.xlsx'
    df.to_excel(response, index=False)
    return response

def export_products_to_excel(request):
    products = AriclesModel.objects.all().values()
    df = pd.DataFrame(products)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=products.xlsx'
    df.to_excel(response, index=False)
    return response

def export_sales_to_excel(request):
    sales = VenteModel.objects.all().values()
    df = pd.DataFrame(sales)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=sales.xlsx'
    df.to_excel(response, index=False)
    return response

def export_achats_to_excel(request):
    achats = AchatModel.objects.all().values()
    df = pd.DataFrame(achats)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=achats.xlsx'
    df.to_excel(response, index=False)
    return response

# CRUD for Clients
def InsertClient(request):
    if request.method == 'POST':
        form = Clientforms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client added successfully.')
            return redirect('clients_table')
    else:
        form = Clientforms()
    return render(request, 'clients_table.html', {'form': form})

def EditClient(request, client_id):
    client = get_object_or_404(ClientModel, client_id=client_id)
    if request.method == 'POST':
        form = Clientforms(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client updated successfully.')
            return redirect('clients_table')
    else:
        form = Clientforms(instance=client)
    return render(request, 'clients_table.html', {'form': form})

def DeleteClient(request, client_id):
    client = get_object_or_404(ClientModel, client_id=client_id)
    client.delete()
    messages.success(request, 'Client deleted successfully.')
    return redirect('clients_table')

def show_clients_table(request):
    clients = ClientModel.objects.all()

    city_filter = request.GET.get('city', '')
    machine_filter = request.GET.get('machine', '')
    search_query = request.GET.get('search', '')

    if city_filter:
        clients = clients.filter(ville=city_filter)
    
    if machine_filter in ['True', 'False']:
        machine_bool = machine_filter == 'True'
        clients = clients.filter(machine=machine_bool)

    if search_query:
        clients = clients.filter(nom__icontains=search_query)

    context = {
        'clients': clients,
        'city_filter': city_filter,
        'machine_filter': machine_filter,
        'search_query': search_query,
    }
    return render(request, 'clients_table.html', context)

# CRUD for Achat
def InsertAchat(request):
    if request.method == 'POST':
        form = Achatforms(request.POST)
        if form.is_valid():
            saverecord = form.save(commit=False)
            max_num = AchatModel.objects.all().aggregate(Max('num'))['num__max']
            saverecord.num = (max_num + 1) if max_num is not None else 1
            saverecord.save()
            messages.success(request, f'Achat {saverecord.num} Is Saved Successfully')
            return redirect('achat_table')
    else:
        form = Achatforms()
    return render(request, 'achat_table.html', {'form': form})

def EditAchat(request, num):
    editempobj = get_object_or_404(AchatModel, num=num)
    data = {
        "art_id": editempobj.art_id,
        "qte": editempobj.qte,
        "date": editempobj.date.strftime('%Y-%m-%d')
    }
    return JsonResponse(data)

def UpdateAchat(request, num):
    Updateemp = get_object_or_404(AchatModel, num=num)
    if request.method == 'POST':
        form = Achatforms(request.POST, instance=Updateemp)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record Updated Successfully.')
            return redirect('achat_table')
        else:
            messages.error(request, 'Error updating the record.')
    else:
        form = Achatforms(instance=Updateemp)
    return render(request, 'achat_table.html', {"form": form, "articles": AriclesModel.objects.all()})

def show_achat_table(request):
    showall = AchatModel.objects.all()
    articles = AriclesModel.objects.all()
    return render(request, 'achat_table.html', {"data": showall, "articles": articles})

def DelAchat(request, num):
    delemployee = get_object_or_404(AchatModel, num=num)
    delemployee.delete()
    messages.success(request, f'Achat {num} Deleted Successfully')
    return redirect('achat_table')

# CRUD for Articles
def InsertArticles(request):
    if request.method == 'POST':
        lib = request.POST.get('lib')
        pu = request.POST.get('pu')
        
        if lib and pu:
            # Automatically set the next art_id value
            max_art_id = AriclesModel.objects.all().aggregate(Max('art_id'))['art_id__max']
            next_art_id = (max_art_id + 1) if max_art_id is not None else 1

            saverecord = AriclesModel(art_id=next_art_id, lib=lib, pu=pu)
            saverecord.save()
            messages.success(request, f'Article {saverecord.art_id} Is Saved Successfully')
            return redirect('articles_table')  # Redirect to avoid re-submitting the form on refresh
    return render(request, 'articles_table.html')

def EditArticles(request, art_id):
    editempobj = get_object_or_404(AriclesModel, art_id=art_id)
    data = {
        "art_id": editempobj.art_id,
        "lib": editempobj.lib,
        "pu": editempobj.pu
    }
    return JsonResponse(data)

def updateArticles(request, art_id):
    Updateemp = get_object_or_404(AriclesModel, art_id=art_id)
    if request.method == 'POST':
        form = Articlesforms(request.POST, instance=Updateemp)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record Updated Successfully.')
            return redirect('articles_table')
        else:
            messages.error(request, 'Error updating the record.')
    else:
        form = Articlesforms(instance=Updateemp)
    return render(request, 'articles_table.html', {"form": form, "dataa": AriclesModel.objects.all()})

def DelArticles(request, art_id):
    delemployee = get_object_or_404(AriclesModel, art_id=art_id)
    delemployee.delete()
    messages.success(request, f'Article {art_id} Deleted Successfully')
    return redirect('articles_table')

def show_articles_table(request):
    showall = AriclesModel.objects.all()
    return render(request, 'articles_table.html', {"dataa": showall})

# CRUD for Ventes and PDF generation
def InsertVentes(request):
    if request.method == 'POST':
        form = Venteforms(request.POST)
        if form.is_valid():
            saverecord = form.save(commit=False)
            max_num = VenteModel.objects.all().aggregate(Max('num'))['num__max']
            saverecord.num = (max_num + 1) if max_num is not None else 1
            saverecord.save()
            messages.success(request, f'Vente {saverecord.num} Is Saved Successfully')

            # Retrieve the article using the article id
            article = get_object_or_404(AriclesModel, art_id=saverecord.art_id)

            # Generate the bill
            bill = {
                'num': saverecord.num,
                'article': article.lib,
                'quantity': saverecord.qte,
                'price': article.pu,
                'total': saverecord.qte * article.pu,
                'date': saverecord.date
            }

            if 'download_pdf' in request.GET:
                # Render the HTML template with bill context
                template = get_template('bill_pdf.html')
                html = template.render({'bill': bill})

                # Create a response object for PDF
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="bill_{saverecord.num}.pdf"'

                # Generate PDF
                pisa_status = pisa.CreatePDF(html, dest=response)
                if pisa_status.err:
                    return HttpResponse(f'We had some errors <pre>{html}</pre>')
                return response

            return render(request, 'bill.html', {'bill': bill})
    else:
        form = Venteforms()
    return render(request, 'ventes_table.html', {'form': form})

def EditVentes(request, num):
    editempobj = get_object_or_404(VenteModel, num=num)
    data = {
        "art_id": editempobj.art_id,
        "qte": editempobj.qte,
        "date": editempobj.date.strftime('%Y-%m-%d')
    }
    return JsonResponse(data)

def updateVentes(request, num):
    Updateemp = get_object_or_404(VenteModel, num=num)
    if request.method == 'POST':
        form = Venteforms(request.POST, instance=Updateemp)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record Updated Successfully.')
            return redirect('ventes_table')
        else:
            messages.error(request, 'Error updating the record.')
    else:
        form = Venteforms(instance=Updateemp)
    return render(request, 'ventes_table.html', {"form": form, "dataaa": VenteModel.objects.all()})

def DelVentes(request, num):
    delemployee = get_object_or_404(VenteModel, num=num)
    delemployee.delete()
    messages.success(request, f'Vente {num} Deleted Successfully')
    return redirect('ventes_table')

def show_ventes_table(request):
    showall = VenteModel.objects.all()
    return render(request, 'ventes_table.html', {"dataaa": showall})

# Bilan calculation
def calculate_bilan():
    bilans = []
    articles = AriclesModel.objects.all()
    for article in articles:
        total_achats = AchatModel.objects.filter(art_id=article.art_id).aggregate(Sum('qte'))['qte__sum'] or 0
        total_ventes = VenteModel.objects.filter(art_id=article.art_id).aggregate(Sum('qte'))['qte__sum'] or 0
        qte_actuelle = total_achats - total_ventes
        bilans.append({
            'num': article.art_id,  # Using article ID as a placeholder for Num
            'art_id': article.art_id,
            'qte_actuelle': qte_actuelle
        })
    return bilans

def update_bilan_table():
    article_ids = set(AchatModel.objects.values_list('art_id', flat=True)) | set(VenteModel.objects.values_list('art_id', flat=True))
    for art_id in article_ids:
        total_achats = AchatModel.objects.filter(art_id=art_id).aggregate(Sum('qte'))['qte__sum'] or 0
        total_ventes = VenteModel.objects.filter(art_id=art_id).aggregate(Sum('qte'))['qte__sum'] or 0
        qte_actuelle = total_achats - total_ventes
        Bilan.objects.update_or_create(
            art_id=art_id,
            defaults={'qte_actuelle': qte_actuelle}
        )

# Dashboard and Analytics
def sidebar_view(request):
    return render(request, 'sidebar2.html')

def analytic(request):
    return render(request, 'analytic.html')

def dashboard(request):
    bilans = calculate_bilan()
    total_articles = AriclesModel.objects.count()
    total_sales = VenteModel.objects.aggregate(Sum('qte'))['qte__sum'] or 0
    total_purchases = AchatModel.objects.aggregate(Sum('qte'))['qte__sum'] or 0
    context = {
        "bilans": bilans,
        "total_articles": total_articles,
        "total_sales": total_sales,
        "total_purchases": total_purchases
    }
    return render(request, 'dashboard.html', context)

# File Upload and Processing
def get_postgres_type(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return 'INTEGER'
    elif pd.api.types.is_float_dtype(dtype):
        return 'FLOAT'
    elif pd.api.types.is_bool_dtype(dtype):
        return 'BOOLEAN'
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return 'TIMESTAMP'
    else:
        return 'TEXT'

def upload_file(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            file = request.FILES['file']
            try:
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                file_path = fs.path(filename)
                xls = pd.ExcelFile(file_path)
                sheet_names = xls.sheet_names
                for sheet in sheet_names:
                    df = pd.read_excel(xls, sheet_name=sheet)
                    with connection.cursor() as cursor:
                        columns = df.columns
                        table_name = sheet.lower()
                        column_types = [get_postgres_type(dtype) for dtype in df.dtypes]
                        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join([f'{col} {col_type}' for col, col_type in zip(columns, column_types)])})"
                        cursor.execute(create_table_query)
                        for index, row in df.iterrows():
                            insert_row_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"
                            cursor.execute(insert_row_query, tuple(row))
                messages.success(request, 'File uploaded and data imported successfully!')
                update_bilan_table()
            except Exception as e:
                messages.error(request, f'Error processing file: {str(e)}')
            finally:
                if xls:
                    xls.close()
                if os.path.exists(file_path):
                    os.remove(file_path)
        else:
            messages.error(request, 'No file uploaded. Please upload a valid Excel file.')
    return render(request, 'upload.html')
