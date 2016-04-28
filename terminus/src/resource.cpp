#include <terminus/resource.h>

namespace terminus
{
namespace resources
{
    resource_ptr serialize(uint64_t id, uint8_t payload[], uint64_t payload_size)
    {
    }

    template<class T> std::shared_ptr<T> deserialize(const resource_ptr resource)
    {
    }
}   // namespace resources
}   // namespace terminus
