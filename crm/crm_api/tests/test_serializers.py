import pytest
import factory

from crm_api.serializers import ClientSerializer, ContractSerializer, EventSerializer
from crm_api.factories import SalesContactFactory, ClientFactory, ContractFactory, EventFactory


class TestClientSerializer:

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_serialize_model(self):
        client = ClientFactory.build()
        serializer = ClientSerializer(client)

        assert serializer.data

    @pytest.mark.unit
    def test_serialized_data(self):
        valid_serialized_data = factory.build(
            dict,
            FACTORY_CLASS=ClientFactory
        )
        serializer = ClientSerializer(data=valid_serialized_data)

        assert serializer.is_valid()
        assert serializer.errors == {}


class TestContractSerializer:

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_serialize_model(self):
        contract = ContractFactory.build()
        serializer = ContractSerializer(contract)

        assert serializer.data

    @pytest.mark.unit
    def test_serialized_data(self):
        valid_serialized_data = factory.build(
            dict,
            FACTORY_CLASS=ContractFactory
        )
        serializer = ContractSerializer(data=valid_serialized_data)

        assert serializer.is_valid()
        assert serializer.errors == {}


class TestEventSerializer:

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_serialize_model(self):
        event = EventFactory.build()
        serializer = EventSerializer(event)

        assert serializer.data

    @pytest.mark.unit
    def test_serialized_data(self):
        valid_serialized_data = factory.build(
            dict,
            FACTORY_CLASS=EventFactory
        )
        serializer = EventSerializer(data=valid_serialized_data)

        assert serializer.is_valid()
        assert serializer.errors == {}
