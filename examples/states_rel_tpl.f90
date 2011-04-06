module states_rel

use types
use utils
implicit none
private
public get_atomic_states_rel, get_RLDA_energies

contains

subroutine get_atomic_states_rel(Z, no, lo, so, fo)
! Returns all electron states of the form (n, l, f) for a given Z
integer, intent(in) :: Z ! atomic number
integer, intent(out), allocatable :: no(:), lo(:) ! quantum numbers "n" and "l"
integer, intent(out), allocatable :: so(:) ! spin (+1 or -1)
real(dp), intent(out), allocatable :: fo(:) ! occupancy of the (n, l) state
! Note: sum(fo) == Z

integer :: n

select case (Z)
{% for s in states %}
    case ({{ s.Z }})
        n = {{ s.len_n }}
        allocate(no(n), lo(n), so(n), fo(n))
        no = (/ {% for x in s.n %}{{ x }}{% if not loop.last %}, {% endif %}{% endfor %} /)
        lo = (/ {% for x in s.l %}{{ x }}{% if not loop.last %}, {% endif %}{% endfor %} /)
        so = (/ {% for x in s.s %}{{ x }}{% if not loop.last %}, {% endif %}{% endfor %} /)
        fo = (/ &{% for x in s.f %}
            {{ x }}_dp{% if not loop.last %}, {% endif %} &{% endfor %}
            /)
{% endfor %}
    case default
        call stop_error("Z = " // str(Z) // " not supported.")
end select
end subroutine

subroutine get_RLDA_energies(Z, E)
integer, intent(in) :: Z
real(dp), intent(out) :: E(:)

integer :: n

select case (Z)
{% for s in states %}
    case ({{ s.Z }})
        n = {{ s.len_n }}
        if (size(E) /= n) call stop_error("get_LDA_energies: wrong len(E)")
        E = (/ &{% for x in s.ks_energies %}
            {{ x }}_dp{% if not loop.last %}, {% endif %} &{% endfor %}
            /)
{% endfor %}
    case default
        call stop_error("Z = " // str(Z) // " not supported.")
end select
end subroutine

end module
