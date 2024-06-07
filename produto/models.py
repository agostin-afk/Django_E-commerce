from django.conf import settings
from django.db import models
from django.utils.text import slugify
from utils import formatacao 
from PIL import Image
import os

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    imagem = models.ImageField(
        upload_to='produto_imagens/%Y/%m/', blank=True, null=True)
    slug = models.SlugField(unique=True,blank=True, null=True)
    preco_marketing = models.FloatField(default=0, verbose_name='preço')
    preco_marketing_promocao = models.FloatField(default=0, verbose_name='preço promo')
    tipo = models.CharField(
            default='V',
            max_length=1,
            choices=(
                ('V', 'Variável'),
                ('S', 'Simples')
                )  
            )
    
    def formatar_descricao_curta(self):
        if len(self.descricao_curta)> 172:
            return f'{self.descricao_curta.strip()[:172]}...'
    formatar_descricao_curta.short_description = 'descricao_curta'
    
    def get_preco_formatado(self):
        return formatacao.formata_preco(self.preco_marketing)
    get_preco_formatado.short_description = 'Preço'
    
    
    def get_preco_promo_formatado(self):
        return formatacao.formata_preco(self.preco_marketing_promocao)
    get_preco_promo_formatado.short_description = 'Preço promo'


    def resize_image(self, img, new_width=800):
        
        img_full_path= os.path.join(settings.MEDIA_ROOT, img.name)
        img_pillow = Image.open(img_full_path)
        original_width,original_height = img_pillow.size
        if original_width <= new_width:
            img_pillow.close(
            )
            return
            
        new_height = round((new_width * original_height) / original_width)
        
        new_img = img_pillow.resize((new_width, new_height),Image.LANCZOS) # type: ignore
        
        new_img.save(
            img_full_path,
            optimize=True,
            quality=50,
        )
        
        print('Imagem redimencionada')
   
   
    def save(self, *args, **kwargs):
        if not self.slug:
            super().save(*args, **kwargs)
            self.slug = f'{slugify(self.nome)}-{self.pk}'
        super().save(*args, **kwargs)
        max_image_size = 800
        if self.imagem: 
            self.resize_image(self.imagem, max_image_size)
    
    def __str__(self):
        return self.nome


class Variacao(models.Model):
    
    class Meta:
        verbose_name= 'Variação'
        verbose_name_plural= 'Variações'
    
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, blank= True, null= True)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return self.nome or self.produto.nome