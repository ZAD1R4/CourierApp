import pytest
from fastapi import HTTPException
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

# Добавляем корень проекта в PYTHONPATH
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

# Правильные импорты
from routes.locations import update_location
from models import LocationUpdate

@pytest.fixture
def mock_db():
    """Фикстура для мокирования базы данных"""
    with patch("routes.locations.db") as mock:
        yield mock

@pytest.fixture
def mock_get_current_user():
    """Фикстура для мокирования функции получения текущего пользователя"""
    with patch("routes.locations.get_current_user") as mock:
        yield mock

@pytest.mark.asyncio
async def test_update_location_success(mock_db, mock_get_current_user):
    test_data = {
        "courier_id": "courier123",
        "latitude": 55.7558,
        "longitude": 37.6176
    }
    location_update = LocationUpdate(**test_data)
    
    mock_get_current_user.return_value = {"role": "courier", "user_id": "courier123"}
    mock_db.locations.update_one = MagicMock()
    
    with patch("routes.locations.datetime") as mock_datetime:
        # Используем timezone-aware datetime
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        response = await update_location(
            location=location_update,
            current_user=mock_get_current_user.return_value
        )
    
    mock_db.locations.update_one.assert_called_once_with(
        {"courier_id": "courier123"},
        {"$set": {
            "latitude": 55.7558,
            "longitude": 37.6176,
            "timestamp": datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        }},
        upsert=True
    )

@pytest.mark.asyncio
async def test_update_location_forbidden(mock_get_current_user):
    """Тест запрета обновления местоположения для не-курьеров"""
    # Подготовка тестовых данных
    test_data = {
        "courier_id": "courier123",
        "latitude": 55.7558,
        "longitude": 37.6176
    }
    location_update = LocationUpdate(**test_data)
    
    # Настройка мока (пользователь - не курьер)
    mock_get_current_user.return_value = {"role": "customer", "user_id": "user123"}
    
    # Проверка вызова исключения
    with pytest.raises(HTTPException) as exc_info:
        await update_location(
            location=location_update,
            current_user=mock_get_current_user.return_value
        )
    
    # Проверки ошибки
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Only couriers can update location"

@pytest.mark.asyncio
async def test_update_location_db_error(mock_db, mock_get_current_user):
    """Тест обработки ошибки базы данных"""
    # Подготовка тестовых данных
    test_data = {
        "courier_id": "courier123",
        "latitude": 55.7558,
        "longitude": 37.6176
    }
    location_update = LocationUpdate(**test_data)
    
    # Настройка моков
    mock_get_current_user.return_value = {"role": "courier", "user_id": "courier123"}
    
    # Создаем специфическое исключение для теста
    test_exception = Exception("Database connection error")
    mock_db.locations.update_one.side_effect = test_exception
    
    # Проверка вызова исключения
    with pytest.raises(HTTPException) as exc_info:
        await update_location(
            location=location_update,
            current_user=mock_get_current_user.return_value
        )
    
    # Проверки ошибки
    assert exc_info.value.status_code == 500
    assert "Database connection error" in str(exc_info.value.detail)
    mock_db.locations.update_one.assert_called_once()