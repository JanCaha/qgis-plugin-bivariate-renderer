from qgis.core import (QgsProcessingAlgorithm, QgsProcessingParameterVectorLayer, QgsProcessing,
                       QgsProcessingParameterNumber, QgsProcessingParameterField,
                       QgsProcessingParameterString, QgsField, QgsClassificationEqualInterval)
from qgis.PyQt.QtCore import (QVariant)


class CalculateCategoriesAlgorithm(QgsProcessingAlgorithm):

    INPUT_LAYER = "InputLayer"
    NUMBER_CLASSES = "NumberOfClasses"
    FIELD_1 = "Field1"
    FIELD_2 = "Field2"
    RESULT_FIELD_NAME = "ResultFieldName"

    def initAlgorithm(self, config=None):

        self.addParameter(
            QgsProcessingParameterVectorLayer(self.INPUT_LAYER, "Input polygon layer",
                                              [QgsProcessing.TypeVectorPolygon]))

        self.addParameter(
            QgsProcessingParameterField(self.FIELD_1,
                                        "Select field 1",
                                        parentLayerParameterName=self.INPUT_LAYER,
                                        type=QgsProcessingParameterField.Numeric))

        self.addParameter(
            QgsProcessingParameterField(self.FIELD_2,
                                        "Select field 2",
                                        parentLayerParameterName=self.INPUT_LAYER,
                                        type=QgsProcessingParameterField.Numeric))

        self.addParameter(
            QgsProcessingParameterNumber(
                self.NUMBER_CLASSES,
                "Number of classes for each field (total number of classes is this nubmer times 2)",
                type=QgsProcessingParameterNumber.Integer,
                minValue=2,
                maxValue=5,
                defaultValue=3))

        self.addParameter(
            QgsProcessingParameterString(self.RESULT_FIELD_NAME,
                                         "Result field name",
                                         defaultValue="Category"))

    def processAlgorithm(self, parameters, context, feedback):

        layer = self.parameterAsVectorLayer(parameters, self.INPUT_LAYER, context)
        field1 = self.parameterAsString(parameters, self.FIELD_1, context)
        field2 = self.parameterAsString(parameters, self.FIELD_2, context)
        number_of_classes = self.parameterAsDouble(parameters, self.NUMBER_CLASSES, context)
        result_field = self.parameterAsString(parameters, self.RESULT_FIELD_NAME, context)

        classification_alg = QgsClassificationEqualInterval()

        layer.startEditing()

        layer.addAttribute(QgsField(result_field, QVariant.String))

        classes_1 = classification_alg.classes(layer, field1, int(number_of_classes))
        classes_2 = classification_alg.classes(layer, field2, int(number_of_classes))

        field_index = layer.fields().indexOf(result_field)

        feature_count = layer.dataProvider().featureCount()

        features_iterator = layer.getFeatures()

        for number, feature in enumerate(features_iterator):

            if feedback.isCanceled():
                break

            field_1_value = feature.attribute(field1)
            field_2_value = feature.attribute(field2)

            for i, range_class in enumerate(classes_1):

                if range_class.lowerBound() <= field_1_value <= range_class.upperBound():
                    class_value_1 = i + 1

            for i, range_class in enumerate(classes_2):

                if range_class.lowerBound() <= field_2_value <= range_class.upperBound():
                    class_value_2 = i + 1

            layer.changeAttributeValue(feature.id(), field_index,
                                       "{}-{}".format(class_value_1, class_value_2))

            feedback.setProgress((number / feature_count) * 100)

        layer.commitChanges()

        return {}

    def name(self):
        return "createcategories"

    def displayName(self):
        return "Create Bivariate Categories"

    def group(self):
        pass

    def groupId(self):
        pass

    def createInstance(self):
        return CalculateCategoriesAlgorithm()
