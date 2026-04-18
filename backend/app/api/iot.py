from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional

router = APIRouter()


class SensorDataRequest(BaseModel):
    device_id: str = Field(..., description="设备 ID")
    sensor_type: str = Field(..., description="传感器类型")
    temperature: Optional[float] = Field(None, description="温度 (°C)")
    humidity: Optional[float] = Field(None, description="湿度 (%)")
    soil_moisture: Optional[float] = Field(None, description="土壤湿度 (%)")
    light: Optional[float] = Field(None, description="光照强度 (lux)")
    co2: Optional[float] = Field(None, description="CO2 浓度 (ppm)")
    value: Optional[float] = Field(None, description="通用值字段")


@router.post("/sensor")
async def receive_sensor_data(request: SensorDataRequest):
    from app.database.influxdb import influxdb_adapter
    sensor_data = request.model_dump()
    await influxdb_adapter.write_sensor_data(sensor_data)
    return {"status": "ok", "message": "传感器数据已接收"}


@router.get("/sensor/{device_id}")
async def query_sensor_data(device_id: str, hours: int = 24):
    from app.database.influxdb import influxdb_adapter
    results = await influxdb_adapter.query_sensor_data(device_id, hours)
    return {"device_id": device_id, "data": results}


@router.post("/device/register")
async def register_device(request: dict):
    return {
        "status": "ok",
        "message": "设备注册成功",
        "device_id": request.get("device_id", "new_device"),
        "api_key": "kiwi_device_api_key_xxx",
    }
