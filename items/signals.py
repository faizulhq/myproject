from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Item

# 1. HAPUS file saat data Item DIHAPUS
@receiver(post_delete, sender=Item)
def delete_item_files_on_delete(sender, instance, **kwargs):
    """
    Menghapus file image dan document dari R2 ketika object Item dihapus dari database.
    """
    # Hapus Gambar
    if instance.image:
        instance.image.delete(save=False)
    
    # Hapus Dokumen
    if instance.document:
        instance.document.delete(save=False)

# 2. HAPUS file lama saat data Item DI-UPDATE (Ganti Gambar/Dokumen)
@receiver(pre_save, sender=Item)
def delete_item_files_on_change(sender, instance, **kwargs):
    """
    Menghapus file lama dari R2 ketika object Item diupdate dengan file baru.
    """
    if not instance.pk:
        return False

    try:
        old_item = Item.objects.get(pk=instance.pk)
    except Item.DoesNotExist:
        return False

    # Logika untuk Image
    new_image = instance.image
    old_image = old_item.image
    
    # Jika ada gambar lama DAN gambar barunya berbeda (diganti)
    if old_image and old_image != new_image:
        old_image.delete(save=False)

    # Logika untuk Document
    new_doc = instance.document
    old_doc = old_item.document
    
    # Jika ada dokumen lama DAN dokumen barunya berbeda (diganti)
    if old_doc and old_doc != new_doc:
        old_doc.delete(save=False)