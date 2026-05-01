from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from config.choices import EstadoEnvio

from .forms import EncomiendaForm
from .models import Empleado, Encomienda


@login_required
def dashboard(request):
    activas = Encomienda.objects.activas().count()
    en_transito = Encomienda.objects.en_transito().count()
    con_retraso = Encomienda.objects.con_retraso().count()
    entregadas = Encomienda.objects.entregadas().count()

    stats = [
        ("Activas", activas, "primary", "boxes"),
        ("En tránsito", en_transito, "info", "truck"),
        ("Con retraso", con_retraso, "danger", "triangle-exclamation"),
        ("Entregadas", entregadas, "success", "check"),
    ]
    ultimas = Encomienda.objects.con_relaciones()[:10]
    return render(request, "index.html/dashboard.html", {"stats": stats, "ultimas": ultimas})


@login_required
def encomienda_lista(request):
    estado = (request.GET.get("estado") or "").strip()
    q = (request.GET.get("q") or "").strip()
    page_number = request.GET.get("page", 1)

    encomiendas = Encomienda.objects.con_relaciones()
    if estado:
        encomiendas = encomiendas.filter(estado=estado)
    if q:
        encomiendas = encomiendas.filter(codigo__icontains=q)

    paginator = Paginator(encomiendas, 15)
    encomiendas_page = paginator.get_page(page_number)

    return render(
        request,
        "index.html/lista.html",
        {
            "encomiendas": encomiendas_page,
            "estado_actual": estado,
            "q": q,
            "estados": EstadoEnvio.choices,
        },
    )


@login_required
def encomienda_detalle(request, pk):
    encomienda = get_object_or_404(Encomienda.objects.con_relaciones(), pk=pk)
    historial = encomienda.historial.select_related("empleado")
    return render(
        request,
        "index.html/detalle.html",
        {"encomienda": encomienda, "historial": historial, "estados": EstadoEnvio.choices},
    )


@login_required
def encomienda_crear(request):
    if request.method == "POST":
        form = EncomiendaForm(request.POST)
        if form.is_valid():
            encomienda = form.save(commit=False)
            if encomienda.costo_envio in (None, 0):
                encomienda.costo_envio = encomienda.calcular_costo()
            encomienda.save()
            messages.success(request, f"Encomienda {encomienda.codigo} registrada correctamente.")
            return redirect("encomienda_detalle", pk=encomienda.pk)
        messages.error(request, "Corrige los errores del formulario.")
    else:
        form = EncomiendaForm()
        empleado = Empleado.objects.filter(estado=1).order_by("apellidos").first()
        if empleado:
            form.fields["empleado_registro"].initial = empleado.pk
    return render(request, "index.html/form.html", {"form": form})


@login_required
def encomienda_cambiar_estado(request, pk):
    encomienda = get_object_or_404(Encomienda, pk=pk)
    if request.method == "POST":
        nuevo_estado = request.POST.get("estado")
        observacion = request.POST.get("observacion", "")
        empleado = Empleado.objects.filter(estado=1).order_by("apellidos").first()
        if not empleado:
            messages.error(request, "No hay empleados activos para registrar el cambio.")
            return redirect("encomienda_detalle", pk=encomienda.pk)
        try:
            encomienda.cambiar_estado(nuevo_estado, empleado, observacion)
            messages.success(request, "Estado actualizado correctamente.")
        except Exception as exc:
            messages.error(request, str(exc))
    return redirect("encomienda_detalle", pk=encomienda.pk)


def home(request):
    return redirect("dashboard")
