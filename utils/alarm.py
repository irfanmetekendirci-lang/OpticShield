from pathlib import Path
import pygame


class SecurityAlarm:

  def __init__(self, sound_file='alarm/alarm.mp3'):
    pygame.mixer.init()
    self.is_loaded = False
    self.is_ringing = False

    # Proje kök dizinini (OpticShield klasörünü) otomatik bulur
    base_dir = Path(__file__).resolve().parent.parent
    sound_path = base_dir / sound_file

    if sound_path.exists():
      try:
        pygame.mixer.music.load(str(sound_path))
        self.is_loaded = True
      except pygame.error as e:
        print(f'⚠️ Pygame ses yükleme hatası: {e}')
    else:
      print(
          f'⚠️ Uyarı: {sound_path} bulunamadı! Lütfen dosya yolunu kontrol edin.'
      )


  def trigger(self):
    """Alarmı çaldırır (Eğer ses yüklüyse ve çalmıyorsa)"""
    if not self.is_loaded:
      return

    if not self.is_ringing:
      print('🚨 [ALARM SİSTEMİ] Tetiklendi! Alarm çalıyor...')
      pygame.mixer.music.play(-1)
      self.is_ringing = True


  def stop(self):
    """Alarmı susturur (Eğer çalıyorsa)"""
    if self.is_loaded and self.is_ringing:
      print('🛡️ [ALARM SİSTEMİ] Tehlike geçti. Alarm durduruldu.')
      pygame.mixer.music.stop()
      self.is_ringing = False