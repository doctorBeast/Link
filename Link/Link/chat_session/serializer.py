from Link.framework.serializer import Serializer


class ChatSessionSerializer(Serializer):

    def _post_processing(self, obj, result_dict):
        # make custom changes to result_dict:
        members = []
        for member in obj.members:
            temp = {
                "id": str(member.id),
                "name": member.name
            }
            members.append(temp)

        result_dict["members"] = members
